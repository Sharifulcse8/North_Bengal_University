from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import get_db
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = '395196975bb354506f064d37c61cb819'

# ================= UPLOAD CONFIGURATION =================
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ================= STATIC PAGES =================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about-us')
def about():
    return render_template('about.html')

@app.route('/admissions', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        # Personal Info
        name = request.form.get('name')
        father_name = request.form.get('father_name')
        mother_name = request.form.get('mother_name')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        nationality = request.form.get('nationality')
        nid = request.form.get('nid')
        religion = request.form.get('religion')
        
        # Contact Info
        email = request.form.get('email')
        phone = request.form.get('phone')
        present_address = request.form.get('present_address')
        permanent_address = request.form.get('permanent_address')
        
        # Academic Info
        ssc_group = request.form.get('ssc_group')
        ssc_gpa = request.form.get('ssc_gpa')
        hsc_group = request.form.get('hsc_group')
        hsc_gpa = request.form.get('hsc_gpa')
        
        # Program Selection
        department = request.form.get('department')
        program_type = request.form.get('program_type')
        
        # Photo (File)
        photo = request.files.get('photo')
        photo_filename = None
        if photo and photo.filename:
            photo_filename = photo.filename
        
        print(f"""
        ===== NEW ADMISSION APPLICATION =====
        Name: {name}
        Father: {father_name}
        Mother: {mother_name}
        DOB: {dob}
        Gender: {gender}
        Nationality: {nationality}
        NID: {nid}
        Email: {email}
        Phone: {phone}
        Department: {department}
        Program: {program_type}
        SSC: {ssc_group} - GPA: {ssc_gpa}
        HSC: {hsc_group} - GPA: {hsc_gpa}
        Photo: {photo_filename}
        ====================================
        """)
        
        flash('Your application has been submitted successfully! We will contact you soon for the admission test.', 'success')
        return redirect(url_for('admission'))
    
    return render_template('admission.html')

@app.route('/contact-us', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        print(f"Name: {name}, Email: {email}, Message: {message}")
        
        flash('Your message has been sent successfully! We will contact you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/academic-departments')
def departments():
    db = get_db()
    teachers = db.execute('SELECT * FROM teachers WHERE is_active = 1 ORDER BY department, name').fetchall()
    db.close()
    return render_template('departments.html', teachers=teachers)

@app.route('/faculty-members')
def teachers():
    department = request.args.get('department')
    db = get_db()
    
    if department:
        teachers_list = db.execute(
            'SELECT * FROM teachers WHERE department = ? AND is_active = 1 ORDER BY name',
            (department,)
        ).fetchall()
    else:
        teachers_list = db.execute('SELECT * FROM teachers WHERE is_active = 1 ORDER BY department, name').fetchall()
    
    db.close()
    return render_template('teachers.html', teachers=teachers_list, department=department)

@app.route('/student-directory')
def students():
    db = get_db()
    students_list = db.execute('SELECT * FROM students WHERE is_active = 1 ORDER BY department, name').fetchall()
    db.close()
    return render_template('students.html', students=students_list)

@app.route('/research-innovation')
def research():
    return render_template('research.html')

@app.route('/latest-news')
def news():
    db = get_db()
    all_news = db.execute('SELECT * FROM notices WHERE is_active = 1 ORDER BY date_posted DESC LIMIT 10').fetchall()
    db.close()
    return render_template('news.html', notices=all_news)

@app.route('/faq-help')
def faq():
    return render_template('faq.html')

@app.route('/university-library')
def library():
    return render_template('library.html')

@app.route('/campus-facilities')
def facilities():
    return render_template('facilities.html')

@app.route('/notices-announcements')
def notice():
    db = get_db()
    notices = db.execute('SELECT * FROM notices WHERE is_active = 1 ORDER BY date_posted DESC LIMIT 5').fetchall()
    db.close()
    return render_template('notice.html', notices=notices)

@app.route('/exam-schedule')
def exam_schedule_2026():
    return render_template('exam_schedule.html')

# ================= DYNAMIC PAGES =================

@app.route('/news-details/<int:id>')
def news_detail(id):
    db = get_db()
    news_item = db.execute('SELECT * FROM notices WHERE id = ? AND is_active = 1', (id,)).fetchone()
    db.close()
    
    if not news_item:
        return render_template('news_detail.html', news={'title': 'News Not Found', 'content': 'The requested news article does not exist.', 'date': ''}, id=id)
    
    return render_template('news_detail.html', news=news_item, id=id)

@app.route('/faculty-profile/<int:id>')
def teacher_profile(id):
    db = get_db()
    teacher = db.execute('SELECT * FROM teachers WHERE id = ? AND is_active = 1', (id,)).fetchone()
    db.close()
    
    if not teacher:
        return render_template('teacher_profile.html', teacher={'name': 'Teacher Not Found', 'designation': '', 'department': '', 'email': '', 'phone': '', 'bio': ''}, id=id)
    
    return render_template('teacher_profile.html', teacher=teacher, id=id)

@app.route('/student-profile/<int:id>')
def student_profile(id):
    db = get_db()
    student = db.execute('SELECT * FROM students WHERE id = ? AND is_active = 1', (id,)).fetchone()
    db.close()
    
    if not student:
        return render_template('student_profile.html', student={'name': 'Student Not Found', 'student_id': '', 'department': '', 'session': '', 'cgpa': 0, 'email': '', 'phone': '', 'bio': ''}, id=id)
    
    return render_template('student_profile.html', student=student, id=id)

# ================= ADMIN PANEL =================

@app.route('/admin')
def admin_index():
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/dashboard')
def admin_dashboard():
    db = get_db()
    notice_count = db.execute('SELECT COUNT(*) FROM notices WHERE is_active = 1').fetchone()[0]
    teacher_count = db.execute('SELECT COUNT(*) FROM teachers WHERE is_active = 1').fetchone()[0]
    student_count = db.execute('SELECT COUNT(*) FROM students WHERE is_active = 1').fetchone()[0]
    db.close()
    return render_template('admin/dashboard.html', 
                         notice_count=notice_count,
                         teacher_count=teacher_count,
                         student_count=student_count)

# ===== NOTICE CRUD =====

@app.route('/admin/notices')
def admin_notices():
    db = get_db()
    notices = db.execute('SELECT * FROM notices WHERE is_active = 1 ORDER BY date_posted DESC').fetchall()
    db.close()
    return render_template('admin/notices.html', notices=notices)

@app.route('/admin/notice/add', methods=['GET', 'POST'])
def add_notice():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category', 'General')
        
        db = get_db()
        db.execute(
            'INSERT INTO notices (title, content, category) VALUES (?, ?, ?)',
            (title, content, category)
        )
        db.commit()
        db.close()
        
        flash('Notice added successfully!', 'success')
        return redirect(url_for('admin_notices'))
    
    return render_template('admin/add_notice.html')

@app.route('/admin/notice/edit/<int:id>', methods=['GET', 'POST'])
def edit_notice(id):
    db = get_db()
    notice = db.execute('SELECT * FROM notices WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category', 'General')
        
        db.execute(
            'UPDATE notices SET title = ?, content = ?, category = ? WHERE id = ?',
            (title, content, category, id)
        )
        db.commit()
        db.close()
        
        flash('Notice updated successfully!', 'success')
        return redirect(url_for('admin_notices'))
    
    db.close()
    return render_template('admin/edit_notice.html', notice=notice)

@app.route('/admin/notice/delete/<int:id>')
def delete_notice(id):
    db = get_db()
    db.execute('UPDATE notices SET is_active = 0 WHERE id = ?', (id,))
    db.commit()
    db.close()
    flash('Notice deleted successfully!', 'success')
    return redirect(url_for('admin_notices'))

# ===== TEACHER CRUD =====

@app.route('/admin/teachers')
def admin_teachers():
    db = get_db()
    teachers = db.execute('SELECT * FROM teachers WHERE is_active = 1 ORDER BY department, name').fetchall()
    db.close()
    return render_template('admin/teachers.html', teachers=teachers)

@app.route('/admin/teacher/add', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        name = request.form.get('name')
        designation = request.form.get('designation')
        department = request.form.get('department')
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        bio = request.form.get('bio', '')
        
        # ===== IMAGE UPLOAD =====
        image_filename = 'teacher_default.jpg'
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                import time
                unique_name = f"teacher_{int(time.time())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
                image_filename = unique_name
        
        db = get_db()
        db.execute(
            '''INSERT INTO teachers (name, designation, department, email, phone, bio, image) 
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (name, designation, department, email, phone, bio, image_filename)
        )
        db.commit()
        db.close()
        
        flash('Teacher added successfully!', 'success')
        return redirect(url_for('admin_teachers'))
    
    return render_template('admin/add_teacher.html')

@app.route('/admin/teacher/edit/<int:id>', methods=['GET', 'POST'])
def edit_teacher(id):
    db = get_db()
    teacher = db.execute('SELECT * FROM teachers WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        name = request.form.get('name')
        designation = request.form.get('designation')
        department = request.form.get('department')
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        bio = request.form.get('bio', '')
        
        # ===== IMAGE UPLOAD =====
        image_filename = teacher['image'] if teacher['image'] else 'teacher_default.jpg'
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # Delete old image if not default
                if image_filename != 'teacher_default.jpg':
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                filename = secure_filename(file.filename)
                import time
                unique_name = f"teacher_{int(time.time())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
                image_filename = unique_name
        
        db.execute(
            '''UPDATE teachers SET name = ?, designation = ?, department = ?, email = ?, phone = ?, bio = ?, image = ? 
               WHERE id = ?''',
            (name, designation, department, email, phone, bio, image_filename, id)
        )
        db.commit()
        db.close()
        
        flash('Teacher updated successfully!', 'success')
        return redirect(url_for('admin_teachers'))
    
    db.close()
    return render_template('admin/edit_teacher.html', teacher=teacher)

@app.route('/admin/teacher/delete/<int:id>')
def delete_teacher(id):
    db = get_db()
    # Get image filename before deleting
    teacher = db.execute('SELECT image FROM teachers WHERE id = ?', (id,)).fetchone()
    if teacher and teacher['image'] and teacher['image'] != 'teacher_default.jpg':
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], teacher['image'])
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.execute('UPDATE teachers SET is_active = 0 WHERE id = ?', (id,))
    db.commit()
    db.close()
    flash('Teacher deleted successfully!', 'success')
    return redirect(url_for('admin_teachers'))

# ===== STUDENT CRUD =====

@app.route('/admin/students')
def admin_students():
    db = get_db()
    students = db.execute('SELECT * FROM students WHERE is_active = 1 ORDER BY department, name').fetchall()
    db.close()
    return render_template('admin/students.html', students=students)

@app.route('/admin/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        student_id = request.form.get('student_id')
        department = request.form.get('department')
        session = request.form.get('session')
        cgpa = float(request.form.get('cgpa', 0))
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        bio = request.form.get('bio', '')
        
        # ===== IMAGE UPLOAD =====
        image_filename = 'student_default.jpg'
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                import time
                unique_name = f"student_{int(time.time())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
                image_filename = unique_name
        
        db = get_db()
        db.execute(
            '''INSERT INTO students (name, student_id, department, session, cgpa, email, phone, bio, image) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (name, student_id, department, session, cgpa, email, phone, bio, image_filename)
        )
        db.commit()
        db.close()
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('admin_students'))
    
    return render_template('admin/add_student.html')

@app.route('/admin/student/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    db = get_db()
    student = db.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        name = request.form.get('name')
        student_id = request.form.get('student_id')
        department = request.form.get('department')
        session = request.form.get('session')
        cgpa = float(request.form.get('cgpa', 0))
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        bio = request.form.get('bio', '')
        
        # ===== IMAGE UPLOAD =====
        image_filename = student['image'] if student['image'] else 'student_default.jpg'
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # Delete old image if not default
                if image_filename != 'student_default.jpg':
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                filename = secure_filename(file.filename)
                import time
                unique_name = f"student_{int(time.time())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
                image_filename = unique_name
        
        db.execute(
            '''UPDATE students SET 
                name = ?, 
                student_id = ?, 
                department = ?, 
                session = ?, 
                cgpa = ?, 
                email = ?, 
                phone = ?, 
                bio = ?, 
                image = ? 
               WHERE id = ?''',
            (name, student_id, department, session, cgpa, email, phone, bio, image_filename, id)
        )
        db.commit()
        db.close()
        
        flash('Student updated successfully!', 'success')
        return redirect(url_for('admin_students'))
    
    db.close()
    return render_template('admin/edit_student.html', student=student)

@app.route('/admin/student/delete/<int:id>')
def delete_student(id):
    db = get_db()
    # Get image filename before deleting
    student = db.execute('SELECT image FROM students WHERE id = ?', (id,)).fetchone()
    if student and student['image'] and student['image'] != 'student_default.jpg':
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], student['image'])
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.execute('UPDATE students SET is_active = 0 WHERE id = ?', (id,))
    db.commit()
    db.close()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('admin_students'))

# ================= SITEMAP & ROBOTS =================

@app.route('/sitemap.xml')
def sitemap():
    return app.send_static_file('sitemap.xml')

@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')

# ================= RUN =================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)