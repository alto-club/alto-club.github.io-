// ============================================================
// LUMINA - קובץ JavaScript ראשי
// ============================================================

document.addEventListener('DOMContentLoaded', function () {

  // ============================================================
  // 1. תפריט המובייל - פתיחה וסגירה
  // ============================================================

  const hamburger = document.querySelector('.hamburger');
  const navMenu = document.querySelector('.nav-menu');
  const navLinks = document.querySelectorAll('.nav-menu a');

  if (hamburger && navMenu) {
    // פתיחה/סגירה בלחיצה על ההמבורגר
    hamburger.addEventListener('click', function () {
      const isOpen = navMenu.classList.toggle('active');
      hamburger.classList.toggle('active');
      hamburger.setAttribute('aria-expanded', isOpen);
      document.body.classList.toggle('menu-open', isOpen);
    });

    // סגירת התפריט בלחיצה על קישור
    navLinks.forEach(function (link) {
      link.addEventListener('click', function () {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
        hamburger.setAttribute('aria-expanded', false);
        document.body.classList.remove('menu-open');
      });
    });

    // סגירת התפריט בלחיצה מחוץ לאזור
    document.addEventListener('click', function (e) {
      if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
        hamburger.setAttribute('aria-expanded', false);
        document.body.classList.remove('menu-open');
      }
    });
  }

  // ============================================================
  // 2. גלילה חלקה לעוגנים (Smooth Scroll)
  // ============================================================

  const anchorLinks = document.querySelectorAll('a[href^="#"]');

  anchorLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');

      // התעלמות מקישורים ריקים (#)
      if (targetId === '#') return;

      const targetElement = document.querySelector(targetId);

      if (targetElement) {
        e.preventDefault();

        // גובה הנאב-בר לפיצוי
        const navbar = document.querySelector('.navbar') || document.querySelector('header');
        const navbarHeight = navbar ? navbar.offsetHeight : 0;
        const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navbarHeight;

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  // ============================================================
  // 3. כפתור WhatsApp צף
  // ============================================================

  const whatsappNumber = '972501234567';
  const whatsappMessage = encodeURIComponent('שלום, אשמח לקבל מידע נוסף על LUMINA');

  // יצירת הכפתור דינמית
  const whatsappBtn = document.createElement('a');
  whatsappBtn.href = `https://wa.me/${whatsappNumber}?text=${whatsappMessage}`;
  whatsappBtn.target = '_blank';
  whatsappBtn.rel = 'noopener noreferrer';
  whatsappBtn.className = 'whatsapp-float';
  whatsappBtn.setAttribute('aria-label', 'פתח שיחת WhatsApp');
  whatsappBtn.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28" fill="white">
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15
               -.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075
               -.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059
               -.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52
               .149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52
               -.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51
               -.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372
               -.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074
               .149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625
               .712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413
               .248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
      <path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.117 1.526 5.847L.057 23.882
               a.5.5 0 0 0 .613.613l6.115-1.605A11.945 11.945 0 0 0 12 24
               c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 0 1-5.013-1.375
               l-.36-.214-3.733.979.996-3.648-.235-.374A9.818 9.818 0 1 1 12 21.818z"/>
    </svg>
    <span class="whatsapp-tooltip">דברו איתנו!</span>
  `;

  document.body.appendChild(whatsappBtn);

  // הצגת הכפתור אחרי גלילה קטנה
  window.addEventListener('scroll', function () {
    if (window.pageYOffset > 300) {
      whatsappBtn.classList.add('visible');
    } else {
      whatsappBtn.classList.remove('visible');
    }
  });

  // ============================================================
  // 4. טופס הרשמה - ולידציה והודעת תודה
  // ============================================================

  const registrationForm = document.querySelector('#registration-form, .registration-form, form[data-form="register"]');

  if (registrationForm) {

    // פונקציית עזר: הצגת שגיאה לשדה
    function showError(field, message) {
      const existingError = field.parentNode.querySelector('.error-message');
      if (existingError) existingError.remove();

      field.classList.add('error');
      field.classList.remove('success');

      const errorEl = document.createElement('span');
      errorEl.className = 'error-message';
      errorEl.textContent = message;
      errorEl.setAttribute('role', 'alert');
      field.parentNode.appendChild(errorEl);
    }

    // פונקציית עזר: ניקוי שגיאה לשדה
    function clearError(field) {
      const existingError = field.parentNode.querySelector('.error-message');
      if (existingError) existingError.remove();
      field.classList.remove('error');
      field.classList.add('success');
    }

    // ולידציה של שדה בודד
    function validateField(field) {
      const value = field.value.trim();
      const type = field.type;
      const name = field.name;

      // שדה חובה
      if (field.required && !value) {
        showError(field, 'שדה זה הוא חובה');
        return false;
      }

      // ולידציה לפי סוג שדה
      if (value) {
        if (type === 'email') {
          const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailPattern.test(value)) {
            showError(field, 'כתובת המייל אינה תקינה');
            return false;
          }
        }

        if (type === 'tel' || name === 'phone') {
          const phonePattern = /^[\d\s\-+()]{7,15}$/;
          if (!phonePattern.test(value)) {
            showError(field, 'מספר הטלפון אינו תקין');
            return false;
          }
        }

        if ((name === 'name' || name === 'fullname' || name === 'full_name') && value.length < 2) {
          showError(field, 'השם חייב להכיל לפחות 2 תווים');
          return false;
        }

        if (type === 'password') {
          if (value.length < 6) {
            showError(field, 'הסיסמה חייבת להכיל לפחות 6 תווים');
            return false;
          }
        }
      }

      clearError(field);
      return true;
    }

    // ולידציה בזמן אמת (blur)
    const formFields = registrationForm.querySelectorAll('input, select, textarea');
    formFields.forEach(function (field) {
      field.addEventListener('blur', function () {
        validateField(this);
      });

      // ניקוי שגיאה בעת הקלדה
      field.addEventListener('input', function () {
        if (this.classList.contains('error')) {
          const existingError = this.parentNode.querySelector('.error-message');
          if (existingError) existingError.remove();
          this.classList.remove('error');
        }
      });
    });

    // שליחת הטופס
    registrationForm.addEventListener('submit', function (e) {
      e.preventDefault();

      let isValid = true;

      // בדיקת כל השדות
      formFields.forEach(function (field) {
        if (field.tagName !== 'BUTTON' && field.type !== 'submit') {
          if (!validateField(field)) {
            isValid = false;
          }
        }
      });

      if (isValid) {
        // הסתרת הטופס והצגת הודעת תודה
        showThankYouMessage(registrationForm);
      } else {
        // גלילה לשגיאה הראשונה
        const firstError = registrationForm.querySelector('.error');
        if (firstError) {
          firstError.focus();
          firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }
    });

    // הצגת הודעת תודה
    function showThankYouMessage(form) {
      const thankYouDiv = document.createElement('div');
      thankYouDiv.className = 'thank-you-message';
      thankYouDiv.setAttribute('role', 'status');
      thankYouDiv.innerHTML = `
        <div class="thank-you-icon">✓</div>
        <h3>תודה שנרשמת ל-LUMINA