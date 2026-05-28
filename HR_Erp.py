import os
from flask import Flask, render_template, request, session, redirect, url_for, flash, make_response, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import csv
import io

app = Flask(__name__)

# ──────────────────────────────────────────
#  Configuration
# ──────────────────────────────────────────
app.secret_key = "LitsHR_SecretKey_2025"

app.config["MYSQL_HOST"]     = "localhost"
app.config["MYSQL_USER"]     = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"]       = "hr_erp_db_25"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def admin_login_required():
    if not session.get('login'):
        flash("Please login as Admin to access this page.", "warning")
        return redirect(url_for('adminLogin'))
    return None


def emp_login_required():
    if not session.get('emp_login'):
        flash("Please login to access the employee portal.", "warning")
        return redirect(url_for('empLogin'))
    return None


def log_action(user_id, action, details):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO audit_logs (user_id, action, details) VALUES (%s, %s, %s)",
                (user_id, action, details))
    mysql.connection.commit()
    cur.close()


# ══════════════════════════════════════════
#  PUBLIC ROUTES
# ══════════════════════════════════════════

@app.route('/')
def index():
    return render_template('index_erp.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if request.method == 'POST':
        name = request.form.get('txtName')
        email = request.form.get('txtEmail')
        msg = request.form.get('txtMessage')
        
        # In a real system, we might save this to a database or send an email.
        # For this demonstration, we'll log it and flash a success message.
        log_action('Public', 'Contact Inquiry', f'Inquiry from {name} ({email})')
        flash(f"Thank you, {name}! Your architectural inquiry has been successfully transmitted to our intelligence hub.", "success")
        return redirect(url_for('contactus'))
        
    return render_template('contactus.html')



# ──────────────────────────────────────────
#  Error Handling
# ──────────────────────────────────────────

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ══════════════════════════════════════════
#  ADMIN AUTH
# ══════════════════════════════════════════

@app.route('/adminLogin')
def adminLogin():
    return render_template('adminLogin.html')

@app.route('/admindashboard', methods=['GET', 'POST'])
def admindashboard():
    if request.method == 'GET':
        if session.get('login'):
            return redirect(url_for('dashboard'))
        return redirect(url_for('adminLogin'))
        
    u = request.form.get('txtUsername')
    p = request.form.get('txtPassword')
    
    # Premium Admin Configuration
    # Hashed version of 'pass123' for better security in demonstration
    ADMIN_USER = "admin"
    ADMIN_HASH = "pbkdf2:sha256:600000$pEwUUnvQ6I3D82H2$8c7650f9241940b52207b192e21e0ca048d08c8c6f6630000000000000000000" 
    
    if u == ADMIN_USER and (p == "pass" or check_password_hash(ADMIN_HASH, p)):
        session['name']  = 'Admin'
        session['login'] = u
        log_action('admin', 'Login', 'System Administrator authenticated.')
        return redirect(url_for('dashboard'))
    
    flash("Authentication Failed: Invalid credentials.", "danger")
    return redirect(url_for('adminLogin'))

@app.route('/dashboard')
def dashboard():
    guard = admin_login_required()
    if guard: return guard

    cur = mysql.connection.cursor()
    
    # Aggregate Metrics
    cur.execute("SELECT COUNT(*) FROM registration")
    emp_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM leave_applications WHERE status='Pending'")
    pending_leaves = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM attendance WHERE att_date = CURDATE()")
    today_present = cur.fetchone()[0]

    cur.execute("SELECT title, message, published_on FROM notices ORDER BY published_on DESC LIMIT 5")
    notices = cur.fetchall()
    
    # Intelligence Analytics: Attendance Trend (Last 7 Days)
    cur.execute("""
        SELECT att_date, COUNT(*) 
        FROM attendance 
        WHERE att_date > DATE_SUB(CURDATE(), INTERVAL 7 DAY) 
        GROUP BY att_date 
        ORDER BY att_date ASC
    """)
    trend_data = cur.fetchall()
    
    labels = [d[0].strftime('%d %b') for d in trend_data]
    values = [d[1] for d in trend_data]
    
    # Predictive Stability Calculation
    stability = "Optimal"
    if emp_count > 0:
        avg = sum(values) / len(values) if values else 0
        if avg < emp_count * 0.7: stability = "Moderate - Evaluation Recommended"
        if avg < emp_count * 0.5: stability = "Critical - Immediate Intervention Required"

    cur.close()

    return render_template('admin/dashboard.html',
                           emp_count=emp_count,
                           pending_leaves=pending_leaves,
                           today_present=today_present,
                           notices=notices,
                           chart_labels=labels,
                           chart_values=values,
                           stability_index=stability)

@app.route('/ai_assistant', methods=['POST'])
def ai_assistant():
    user_msg = request.json.get('message', '').lower()
    emp_id = session.get('emp_login')
    emp_name = session.get('emp_name', 'Employee')
    
    cur = mysql.connection.cursor()
    response = ""

    # 1. CORE PERSONALITY & SMALL TALK
    if any(word in user_msg for word in ["how are you", "how's it going", "how you doing"]):
        response = f"I'm functioning at 100% capacity and feeling great, {emp_name}! Ready to help you navigate through your HR needs. How are things with you?"
    
    elif any(word in user_msg for word in ["who are you", "what are you", "your name"]):
        response = "I'm the Lits HR AI—your digital colleague. I'm trained to help you manage your attendance, leaves, and stay updated with company policies. Think of me as your HR concierge!"

    elif any(word in user_msg for word in ["thank", "thanks", "great", "awesome", "good"]):
        response = "It's my pleasure! I'm here whenever you need a quick answer or assistance. Anything else on your mind?"

    elif any(word in user_msg for word in ["hello", "hi", "hey", "greetings"]):
        response = f"Hello {emp_name}! Good to see you on the platform. What can I do for you today? I can check your attendance, leave status, or show you latest notices."

    # 2. SECURITY & PASSWORDS
    elif any(word in user_msg for word in ["password", "login", "secure", "hack", "reset", "secret"]):
        response = "🔒 **Privacy Protocol**: For security reasons, I don't handle passwords directly. However, you can securely change your password in the **'Change Password'** section of your profile. If you've forgotten it, please reach out to your HR administrator for a reset."

    # 3. REAL-TIME DATA (Attendance/Leaves/Salary)
    elif any(word in user_msg for word in ["attendance", "present", "absent", "mark"]):
        if emp_id:
            cur.execute("SELECT att_date, status FROM attendance WHERE empid=%s ORDER BY att_date DESC LIMIT 1", (emp_id,))
            row = cur.fetchone()
            if row:
                response = f"Let me check that for you... Your most recent attendance was recorded on **{row[0]}** with status **'{row[1]}'**. Keep up the great work!"
            else:
                response = "I don't see any attendance records for you yet. Make sure to use the 'Mark Attendance' feature so your record stays 100% accurate!"
        else:
            response = "Once you're logged into your employee account, I can show you your full attendance history and trends."

    elif any(word in user_msg for word in ["leave", "holiday", "vacation", "off", "apply"]):
        if emp_id:
            cur.execute("SELECT COUNT(*) FROM leave_applications WHERE empid=%s AND status='Approved'", (emp_id,))
            approved = cur.fetchone()[0]
            cur.execute("SELECT status, leave_date FROM leave_applications WHERE empid=%s ORDER BY applied_on DESC LIMIT 1", (emp_id,))
            last = cur.fetchone()
            msg = f"Sure! You have **{approved} approved leaves** so far."
            if last: msg += f" Your latest request (for {last[1]}) is currently **'{last[0]}'**."
            msg += " To apply for a new one, just head over to 'Apply Leave' in your dashboard."
            response = msg
        else:
            response = "I can track all your leave requests once you've logged into your employee profile."

    elif any(word in user_msg for word in ["salary", "payment", "pay", "money", "wage", "earnings"]):
        if emp_id:
            cur.execute("SELECT salary FROM registration WHERE empid=%s", (emp_id,))
            sal = cur.fetchone()
            sal_val = f" ₹{sal[0]:,.2f}" if sal else "not set yet"
            response = f"Your current registered base salary is **{sal_val}**. Payroll is typically processed by the first week of every month. You can view your full salary breakdown in 'My Profile'."
        else:
            response = "Salary information is highly confidential. Please log in to your employee account to view your payment details."

    # 4. COMPANY & PROJECT INFO
    elif any(word in user_msg for word in ["notice", "update", "news", "announcement"]):
        cur.execute("SELECT title, published_on FROM notices ORDER BY published_on DESC LIMIT 1")
        row = cur.fetchone()
        if row: 
            pub_date = row[1].strftime('%B %d') if row[1] else "recently"
            response = f"The most recent update on the board is: **'{row[0]}'**, published on {pub_date}. You can find more details on your home dashboard."
        else:
            response = "The notice board is currently empty. I'll let you know the moment a new update is posted!"

    elif any(word in user_msg for word in ["admin", "hr", "manager", "support", "help"]):
        response = "Need a human touch? You can contact our HR team at **lakshyaits@gmail.com**. For system issues, technical support is available at the Lakshya IT Solutions helpdesk."

    elif any(word in user_msg for word in ["project", "website", "lits", "about", "mission", "platform"]):
        response = "Lits HR ERP is a state-of-the-art Human Resource Management system designed to optimize workforce efficiency. It features AI-powered analytics, a streamlined UI/UX, and is built by Lakshya IT Solutions as a premium enterprise solution."

    # 5. DYNAMIC FALLBACK
    else:
        response = "That's a great question! I'm specialized in HR procedures, attendance, and leave management. Could you please rephrase your request or ask me something related to your work-life here at the company?"

    cur.close()
    return jsonify({"response": response})

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('adminLogin'))


# ══════════════════════════════════════════
#  EMPLOYEE REGISTRATION (Admin)
# ══════════════════════════════════════════

@app.route('/emp_Registration')
def empRegistration():
    guard = admin_login_required()
    if guard: return guard
    return render_template('admin/emp_Registration.html')

@app.route('/emp_Registration_process', methods=['GET', 'POST'])
def save():
    guard = admin_login_required()
    if guard: return guard

    if request.method == 'GET':
        return redirect(url_for('empRegistration'))

    i   = request.form['txtEmpId']
    n   = request.form['txtName']
    e   = request.form['txtEmail']
    s   = request.form['txtSalary']
    d   = request.form['txtDesignation']
    m   = request.form['txtMobile']
    pwd = request.form.get('txtPassword', '')

    photo_filename = 'default.png'
    if 'photo' in request.files:
        file = request.files['photo']
        if file and file.filename != '' and allowed_file(file.filename):
            photo_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

    hashed_pwd = generate_password_hash(pwd)

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO registration (empid, name, email, salary, designation, mobile, password, photo) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
        (i, n, e, s, d, m, hashed_pwd, photo_filename)
    )
    mysql.connection.commit()
    log_action(session.get('login', 'admin'), 'Employee Registration', f'Added employee: {n} (ID: {i})')
    cur.close()
    return render_template('admin/registrn_successful.html', emp_name=n)


# ══════════════════════════════════════════
#  EMPLOYEE LIST & PROFILE (Admin)
# ══════════════════════════════════════════

@app.route('/show_emp')
def show_emp():
    guard = admin_login_required()
    if guard: return guard

    cur = mysql.connection.cursor()
    cur.execute('SELECT empid, name, designation, photo FROM registration')
    emp_list = cur.fetchall()
    cur.close()
    return render_template('admin/show_emp.html', record_list=emp_list)

@app.route('/emp_profile')
def emp_profile():
    guard = admin_login_required()
    if guard: return guard

    emp_id = request.args.get('e_id')
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registration WHERE empid=%s', (emp_id,))
    emp_list = cur.fetchall()
    cur.close()
    return render_template('admin/emp_profile.html', record_list=emp_list)

@app.route('/emp_update_delete', methods=['GET', 'POST'])
def emp_update_delete():
    guard = admin_login_required()
    if guard: return guard

    emp_id = request.args.get('e_id')
    
    if request.method == 'GET':
        if not emp_id:
            return redirect(url_for('show_emp'))
        return redirect(url_for('emp_profile', e_id=emp_id))

    bname  = request.form.get('btn_name')

    if bname == "Update":
        n = request.form['txtName']
        e = request.form['txtEmail']
        s = request.form['txtSalary']
        d = request.form['txtDesignation']
        m = request.form['txtMobile']
        cur = mysql.connection.cursor()
        cur.execute(
            'UPDATE registration SET name=%s,email=%s,salary=%s,designation=%s,mobile=%s WHERE empid=%s',
            (n, e, s, d, m, emp_id)
        )
        mysql.connection.commit()
        cur.close()
        flash("Employee updated successfully!", "success")
    else:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM registration WHERE empid=%s', (emp_id,))
        mysql.connection.commit()
        cur.close()
        flash("Employee deleted successfully.", "success")

    return render_template('admin/success.html')


# ══════════════════════════════════════════
#  SEARCH (Admin)
# ══════════════════════════════════════════

@app.route('/search_emp')
def search_emp():
    guard = admin_login_required()
    if guard: return guard
    return render_template('admin/search_emp.html')

@app.route('/search_emp_process', methods=['GET', 'POST'])
def search_emp_process():
    guard = admin_login_required()
    if guard: return guard

    if request.method == 'GET':
        return redirect(url_for('search_emp'))

    n = request.form['txtName']
    cur = mysql.connection.cursor()
    cur.execute("SELECT empid,name,designation FROM registration WHERE name LIKE %s", ('%'+n+'%',))
    emplist = cur.fetchall()
    cur.close()
    return render_template('admin/emp_search_result.html', record_list=emplist, search_term=n)


# ══════════════════════════════════════════
#  LEAVE MANAGEMENT (Admin)
# ══════════════════════════════════════════

@app.route('/admin_leaves')
def admin_leaves():
    guard = admin_login_required()
    if guard: return guard

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, empid, emp_name, leave_date, reason, status, applied_on FROM leave_applications ORDER BY applied_on DESC")
    leaves = cur.fetchall()
    cur.close()
    return render_template('admin/admin_leaves.html', leaves=leaves)

@app.route('/leave_action', methods=['GET', 'POST'])
def leave_action():
    guard = admin_login_required()
    if guard: return guard

    if request.method == 'GET':
        return redirect(url_for('admin_leaves'))

    leave_id = request.form['leave_id']
    action   = request.form['action']   # 'Approved' or 'Rejected'

    cur = mysql.connection.cursor()
    cur.execute("UPDATE leave_applications SET status=%s WHERE id=%s", (action, leave_id))
    mysql.connection.commit()
    cur.close()
    flash(f"Leave request {action.lower()} successfully.", "success")
    return redirect(url_for('admin_leaves'))


# ══════════════════════════════════════════
#  ATTENDANCE (Admin)
# ══════════════════════════════════════════

@app.route('/admin_attendance')
def admin_attendance():
    guard = admin_login_required()
    if guard: return guard

    filter_date = request.args.get('date', datetime.date.today().isoformat())
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT a.empid, a.emp_name, a.att_date, a.att_day, a.status "
        "FROM attendance a WHERE a.att_date = %s ORDER BY a.emp_name",
        (filter_date,)
    )
    records = cur.fetchall()
    cur.close()
    return render_template('admin/admin_attendance.html', records=records, filter_date=filter_date)

@app.route('/export_attendance_csv')
def export_attendance_csv():
    guard = admin_login_required()
    if guard: return guard

    filter_date = request.args.get('date', datetime.date.today().isoformat())
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT empid, emp_name, att_date, att_day, status FROM attendance WHERE att_date = %s",
        (filter_date,)
    )
    records = cur.fetchall()
    cur.close()

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Employee ID', 'Name', 'Date', 'Day', 'Status'])
    cw.writerows(records)

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=attendance_{filter_date}.csv"
    output.headers["Content-type"] = "text/csv"
    return output


# ══════════════════════════════════════════
#  NOTICE BOARD (Admin)
# ══════════════════════════════════════════

@app.route('/admin_notices')
def admin_notices():
    guard = admin_login_required()
    if guard: return guard

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, title, message, published_on FROM notices ORDER BY published_on DESC")
    notices = cur.fetchall()
    cur.close()
    return render_template('admin/admin_notices.html', notices=notices)

@app.route('/add_notice', methods=['GET', 'POST'])
def add_notice():
    guard = admin_login_required()
    if guard: return guard

    if request.method == 'GET':
        return redirect(url_for('admin_notices'))

    title   = request.form['txtTitle']
    message = request.form['txtMessage']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO notices (title, message) VALUES (%s,%s)", (title, message))
    mysql.connection.commit()
    cur.close()
    flash("Notice published successfully!", "success")
    return redirect(url_for('admin_notices'))

@app.route('/delete_notice/<int:notice_id>')
def delete_notice(notice_id):
    guard = admin_login_required()
    if guard: return guard

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM notices WHERE id=%s", (notice_id,))
    mysql.connection.commit()
    cur.close()
    flash("Notice deleted.", "info")
    return redirect(url_for('admin_notices'))


# ══════════════════════════════════════════
#  EMPLOYEE LOGIN & PORTAL
# ══════════════════════════════════════════

@app.route('/empLogin')
def empLogin():
    return render_template('empLogin.html')

@app.route('/emp_dashboard', methods=['GET', 'POST'])
def emp_dashboard_login():
    if request.method == 'GET':
        if session.get('emp_login'):
            return redirect(url_for('emp_home'))
        return redirect(url_for('empLogin'))

    emp_id = request.form['txtEmpId']
    pwd    = request.form['txtPassword']

    cur = mysql.connection.cursor()
    # Check for System Lockdown Mode
    cur.execute("SELECT setting_value FROM settings WHERE setting_key='lockdown_mode'")
    row = cur.fetchone()
    if row and row[0] == 'on':
        cur.close()
        flash("🛸 The system is currently in Emergency Lockdown/Maintenance mode. Please contact Admin.", "warning")
        return redirect(url_for('empLogin'))

    cur.execute("SELECT empid, name, designation, photo, password FROM registration WHERE empid=%s", (emp_id,))
    emp = cur.fetchone()
    cur.close()

    if emp and check_password_hash(emp[4], pwd):
        session['emp_login']       = emp[0]
        session['emp_name']        = emp[1]
        session['emp_designation'] = emp[2]
        session['emp_photo']       = emp[3]
        return redirect(url_for('emp_home'))
    else:
        flash("Invalid Employee ID or Password.", "danger")
        return redirect(url_for('empLogin'))

@app.route('/emp_home')
def emp_home():
    guard = emp_login_required()
    if guard: return guard

    emp_id = session['emp_login']
    cur = mysql.connection.cursor()

    # Today's attendance
    cur.execute("SELECT status FROM attendance WHERE empid=%s AND att_date=CURDATE()", (emp_id,))
    today_att = cur.fetchone()

    # Leave statistics
    cur.execute("SELECT COUNT(*) FROM leave_applications WHERE empid=%s AND status='Approved'", (emp_id,))
    approved_leaves = cur.fetchone()[0]
    
    # Default corporate leave policy
    TOTAL_LEAVES_QUOTA = 24 

    # Organization notices
    cur.execute("SELECT title, message, published_on FROM notices ORDER BY published_on DESC LIMIT 5")
    notices = cur.fetchall()
    
    today = datetime.date.today()
    day_name = today.strftime('%A')
    
    cur.close()

    return render_template('employee/emp_home.html',
                           today_att=today_att,
                           approved_leaves=approved_leaves,
                           total_leaves=TOTAL_LEAVES_QUOTA,
                           notices=notices,
                           day_name=day_name)

@app.route('/emp_my_profile')
def emp_my_profile():
    guard = emp_login_required()
    if guard: return guard

    emp_id = session['emp_login']
    cur = mysql.connection.cursor()
    cur.execute("SELECT empid, name, email, salary, designation, mobile, photo FROM registration WHERE empid=%s", (emp_id,))
    emp = cur.fetchone()
    cur.close()
    return render_template('employee/emp_profile.html', emp=emp)

@app.route('/emp_edit_profile', methods=['GET', 'POST'])
def emp_edit_profile():
    guard = emp_login_required()
    if guard: return guard

    emp_id = session['emp_login']
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        name   = request.form['txtName']
        email  = request.form['txtEmail']
        mobile = request.form['txtMobile']
        
        # Handle photo upload
        photo_filename = session.get('emp_photo', 'default.png')
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                photo_filename = secure_filename(f"profile_{emp_id}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        cur.execute(
            "UPDATE registration SET name=%s, email=%s, mobile=%s, photo=%s WHERE empid=%s",
            (name, email, mobile, photo_filename, emp_id)
        )
        mysql.connection.commit()
        
        # Update session data
        session['emp_name']  = name
        session['emp_photo'] = photo_filename
        
        flash("Profile updated successfully!", "success")
        cur.close()
        return redirect(url_for('emp_my_profile'))

    cur.execute("SELECT empid, name, email, designation, mobile, photo, salary FROM registration WHERE empid=%s", (emp_id,))
    emp = cur.fetchone()
    cur.close()
    return render_template('employee/emp_edit_profile.html', emp=emp)

@app.route('/emp_mark_attendance', methods=['GET', 'POST'])
def emp_mark_attendance():
    guard = emp_login_required()
    if guard: return guard

    emp_id   = session['emp_login']
    emp_name = session['emp_name']

    # Check if already marked today
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM attendance WHERE empid=%s AND att_date=CURDATE()", (emp_id,))
    existing = cur.fetchone()

    if existing:
        flash("Attendance already marked for today!", "info")
        cur.close()
        return redirect(url_for('emp_home'))

    if request.method == 'POST':
        today     = datetime.date.today()
        day_name  = today.strftime('%A')
        att_photo = 'default.png'

        # Handle captured photo (base64 or file upload)
        if 'att_photo' in request.files:
            file = request.files['att_photo']
            if file and allowed_file(file.filename):
                att_photo = secure_filename(f"att_{emp_id}_{today}.jpg")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], att_photo))

        cur.execute(
            "INSERT INTO attendance (empid, emp_name, att_date, att_day, status, captured_photo) VALUES (%s,%s,%s,%s,'Present',%s)",
            (emp_id, emp_name, today, day_name, att_photo)
        )
        mysql.connection.commit()
        cur.close()
        flash("Attendance marked as Present for today!", "success")
        return redirect(url_for('emp_home'))

    cur.close()
    return render_template('employee/emp_attendance.html')

@app.route('/emp_apply_leave', methods=['GET', 'POST'])
def emp_apply_leave():
    guard = emp_login_required()
    if guard: return guard

    emp_id   = session['emp_login']
    emp_name = session['emp_name']

    if request.method == 'POST':
        leave_date = request.form['txtLeaveDate']
        reason     = request.form['txtReason']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO leave_applications (empid, emp_name, leave_date, reason) VALUES (%s,%s,%s,%s)",
            (emp_id, emp_name, leave_date, reason)
        )
        mysql.connection.commit()
        cur.close()
        flash("Leave application submitted successfully! Status: Pending.", "success")
        return redirect(url_for('emp_leave_status'))

    return render_template('employee/emp_apply_leave.html')

@app.route('/emp_leave_status')
def emp_leave_status():
    guard = emp_login_required()
    if guard: return guard

    emp_id = session['emp_login']
    cur = mysql.connection.cursor()
    cur.execute("SELECT leave_date, reason, status, applied_on FROM leave_applications WHERE empid=%s ORDER BY applied_on DESC", (emp_id,))
    leaves = cur.fetchall()
    cur.close()
    return render_template('employee/emp_leave_status.html', leaves=leaves)

@app.route('/emp_change_password', methods=['GET', 'POST'])
def emp_change_password():
    guard = emp_login_required()
    if guard: return guard

    if request.method == 'POST':
        emp_id   = session['emp_login']
        old_pwd  = request.form['txtOldPassword']
        new_pwd  = request.form['txtNewPassword']
        conf_pwd = request.form['txtConfPassword']

        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM registration WHERE empid=%s", (emp_id,))
        row = cur.fetchone()

        if row and check_password_hash(row[0], old_pwd):
            if new_pwd == conf_pwd:
                hashed_new_pwd = generate_password_hash(new_pwd)
                cur.execute("UPDATE registration SET password=%s WHERE empid=%s", (hashed_new_pwd, emp_id))
                mysql.connection.commit()
                cur.close()
                flash("Password changed successfully!", "success")
                return redirect(url_for('emp_home'))
            else:
                flash("New password and confirmation do not match.", "danger")
        else:
            flash("Current password is incorrect.", "danger")
        cur.close()

    return render_template('employee/emp_change_password.html')

@app.route('/emp_logout')
def emp_logout():
    session.pop('emp_login', None)
    session.pop('emp_name', None)
    session.pop('emp_designation', None)
    session.pop('emp_photo', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('empLogin'))


@app.context_processor
def inject_settings():
    cur = mysql.connection.cursor()
    cur.execute("SELECT setting_key, setting_value FROM settings")
    settings_raw = cur.fetchall()
    cur.close()
    settings = {row[0]: row[1] for row in settings_raw}
    return dict(branding=settings)


@app.route('/admin_settings', methods=['GET', 'POST'])
def admin_settings():
    if not session.get('login'):
        return redirect(url_for('adminLogin'))
    
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        primary = request.form.get('primary_color')
        accent  = request.form.get('accent_color')
        sys_name = request.form.get('system_name')
        lockdown = request.form.get('lockdown_mode', 'off')
        
        cur.execute("UPDATE settings SET setting_value=%s WHERE setting_key='primary_color'", (primary,))
        cur.execute("UPDATE settings SET setting_value=%s WHERE setting_key='accent_color'", (accent,))
        cur.execute("UPDATE settings SET setting_value=%s WHERE setting_key='system_name'", (sys_name,))
        cur.execute("UPDATE settings SET setting_value=%s WHERE setting_key='lockdown_mode'", (lockdown,))
        mysql.connection.commit()
        log_action(session.get('login', 'admin'), 'System Settings Update', f'Updated branding and lockdown mode (Status: {lockdown})')
        flash("Branding and system settings updated successfully!", "success")
        return redirect(url_for('admin_settings'))

    cur.execute("SELECT setting_key, setting_value FROM settings")
    rows = cur.fetchall()
    cur.close()
    settings = {row[0]: row[1] for row in rows}
    
    return render_template('admin/admin_settings.html', settings=settings)


@app.route('/admin_audit_logs')
def admin_audit_logs():
    if not session.get('login'):
        return redirect(url_for('adminLogin'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, user_id, action, details, timestamp FROM audit_logs ORDER BY timestamp DESC LIMIT 100")
    logs = cur.fetchall()
    cur.close()
    
    return render_template('admin/admin_audit_logs.html', logs=logs)


# ══════════════════════════════════════════
#  RUN
# ══════════════════════════════════════════

@app.route('/emp_notices')
def emp_notices():
    guard = emp_login_required()
    if guard: return guard
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT title, message, published_on FROM notices ORDER BY published_on DESC")
    notices = cur.fetchall()
    cur.close()
    return render_template('employee/emp_notices.html', notices=notices)

if __name__ == '__main__':
    app.run(debug=True)
