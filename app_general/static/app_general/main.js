console.log('Taowwwwww');

const subscriptionForm=document.querySelector('.subscription-form');

function foodSetValidation(event) {
    const checkedFoodSet = document.querySelectorAll('input[name="food_set"]:checked');
    if (checkedFoodSet.length ===0){
        event.preventDefault();
        alert('Please choose at least one menu');
    }
}
if (!!subscriptionForm){
    subscriptionForm.addEventListener('submit',foodSetValidation);
}

