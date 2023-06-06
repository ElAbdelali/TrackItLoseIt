function updateCount(input, countId, min) {
    var count = input.value.length;
    var countElement = document.getElementById(countId);
  
    if (count < min) {
      countElement.textContent = count + "/" + min + " (needs at least " + (min - count) + " more)";
      countElement.classList.remove('hidden');
    } else {
      countElement.classList.add('hidden');
    }
  }
  
  function checkSpecial(input, specialId) {
    var regex = /[!@#$%^&*(),.?":{}|<>]/;
    var specialElement = document.getElementById(specialId);
  
    if (regex.test(input.value)) {
      specialElement.textContent = "Special character found!";
      specialElement.classList.add('hidden');
    } else {
      specialElement.textContent = "No special characters found!";
      specialElement.classList.remove('hidden');
    }
  }
  
  function checkAge(input, ageId) {
    var dob = new Date(input.value);
    var today = new Date();
    var age = today.getFullYear() - dob.getFullYear();
    var ageElement = document.getElementById(ageId);
  
    if (age < 13) {
      ageElement.textContent = "You must be at least 13 years old!";
      ageElement.classList.remove('hidden');
    } else {
      ageElement.classList.add('hidden');
    }
  }
  