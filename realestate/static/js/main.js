const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

setTimeout(function(){
    $('#message').fadeOut('slow');
}, 3000);

// function phonenumber(inputtxt)
// {
//   var phoneno = /^\d{10}$/;
//   if(inputtxt.value.match(phoneno))
//   {
//       return true;
//   }
//   else
//   {
//      alert("Not a valid Phone Number");
//      return false;
//   }
//   }
