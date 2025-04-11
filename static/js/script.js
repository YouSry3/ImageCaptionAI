document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('uploadForm');
  const fileInput = document.getElementById('imageInput');
  const fileName = document.getElementById('fileName');
  const fileDetails = document.getElementById('fileDetails');
  const generateBtn = document.querySelector('.generate-btn');
  const tabButtons = document.querySelectorAll('.tab-btn');
  const descTexts = document.querySelectorAll('.desc-text');

  // تبديل اللغات
  tabButtons.forEach(btn => {
      btn.addEventListener('click', function() {
          const lang = this.dataset.lang;
          
          tabButtons.forEach(b => b.classList.remove('active'));
          this.classList.add('active');
          
          descTexts.forEach(text => {
              text.classList.remove('active');
              if(text.dataset.lang === lang) {
                  text.classList.add('active');
              }
          });
      });
  });

  // اختيار الملف
  fileInput.addEventListener('change', function() {
      if(this.files.length > 0) {
          const file = this.files[0];
          const fileSize = (file.size / (1024 * 1024)).toFixed(2);
          
          fileName.textContent = file.name;
          fileDetails.textContent = `${file.type.split('/')[1].toUpperCase()} - ${fileSize} MB`;
      }
  });

  // إرسال النموذج
  form.addEventListener('submit', function() {
      if(fileInput.files.length === 0) {
          alert('الرجاء اختيار صورة أولاً');
          return false;
      }
      
      generateBtn.disabled = true;
      generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> جاري المعالجة...';
      return true;
  });
});