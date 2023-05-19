// // Get the form element and add a submit event listener
// const form = document.getElementById('tdee-form');
// form.addEventListener('submit', calculateTDEE);

// // Event handler for the form submit
// function calculateTDEE(event) {
//   event.preventDefault(); // Prevent form submission

//   // Get the form inputs
//   const weight = document.getElementById('weight').value;
//   const height = document.getElementById('height').value;
//   const age = document.getElementById('age').value;
//   const gender = document.getElementById('gender').value;
//   const activityLevel = document.getElementById('activity-level').value;

//   // Create the request payload
//   const payload = {
//     weight: weight,
//     height: height,
//     age: age,
//     gender: gender,
//     activity_level: activityLevel,
//   };

//   // Make the AJAX request
//   fetch('/calculate_tdee', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     body: JSON.stringify(payload),
//   })
//     .then(response => response.json())
//     .then(data => {
//       // Handle the response data
//       console.log(data);
//       // Do something with the data, such as displaying it on the page
//     })
//     .catch(error => {
//       // Handle any errors
//       console.error('Error:', error);
//     });
// }