$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    
    var id = $(this).attr('id');
    //var quantity = $(this).attr('quantity');
    //var quantity = $(this).attr('quantity');

    var eml = this.parentNode.children[2]
    console.log(id)
    $.ajax({
        type:'GET',
        url:'/pluscart',
        data:{
            prod_id: id
        },
        success:function(data){
            eml.innerText = data.quantity;
            console.log(typeof(data.quantity));
            error: (error) => {
                console.log(JSON.stringify(error));
}
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalamount;
            //document.getElementById('quantity').innerText = data.quantity;
        }
    })
})
$('.minus-cart').click(function(){
    
    var id = $(this).attr('id');
    //var quantity = $(this).attr('quantity');
    //var quantity = $(this).attr('quantity');

    var eml = this.parentNode.children[2]
    console.log(id)
    $.ajax({
        type:'GET',
        url:'/minuscart',
        data:{
            prod_id: id
        },
        success:function(data){
            eml.innerText = data.quantity;
            console.log(typeof(data.quantity));
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalamount;
            //document.getElementById('quantity').innerText = data.quantity;
        }
    })
})

$('.remove-cart').click(function(){
    var id = $(this).attr('id');
    var eml = this
    console.log(id)
    $.ajax({
        type:'GET',
        url:'/removecart',
        data:{
            prod_id: id
        },
        success: function (data){
            console.log('delete')
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
        
    })
})

// navbar
window.onscroll = function() {myFunction()};

var navbar = document.getElementById("navbar");
var sticky = navbar.offsetTop;

function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
}