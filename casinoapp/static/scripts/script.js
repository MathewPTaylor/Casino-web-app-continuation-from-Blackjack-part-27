$(document).ready(function() {
    var promo_carousel_index = 0;

    

    // checking if the user is at the homepage (we do this by checking if the sliding promo is in the current DOM)
    document.querySelector('.sliding-promo-rails') ? showCurrentPromoOnly(promo_carousel_index): null;

    document.querySelector('#game-genre-btn-wrapper') ? autoSelectFirstGenre(): null;

    var promo_swiper = new Swiper('.promo', {
      direction: 'horizontal',
      speed: 400  ,

      pagination: {
        el: '.swiper-pagination',
      },

      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
        color: 'white'
      },

      scrollbar: {
        el: '.swiper-scrollbar',
      }
    });

    document.querySelectorAll('.swiper-slide').forEach((slide)=> {
      // console.log(slide);
      slide.style.display = "flex";
    });
  
    function showCurrentPromoOnly(promo_index) {
        // get the 'rail' element
        let rails = document.querySelector('.sliding-promo-rails');

        // unshow all promos except current promo
        for (let i=0; i<rails.children.length; i++) {
            console.log(rails.children[i])
            if (i != promo_index) {
                rails.children[i].style.display = "none";
            }
        }
    }

  
    function autoSelectFirstGenre() {
      let btn_container = document.getElementById("game-genre-btn-wrapper");
      // alert(btn_container);
      let firstChild = btn_container.children[0];
      console.log(firstChild);
      // alert(firstChild.id);
      firstChild.classList.add("selected-btn");
      let gameGenre = firstChild.id;
      console.log(gameGenre);
      let gamesDisp = document.getElementById(gameGenre+"-games");
      console.log(gamesDisp);
    }

  
    $("#nav-user-profile").click(function() {
        // dropdown not shown, at the time of click
        if (this.getAttribute('visible') == "false") {
            // show the dropdown
            let dropdown = document.getElementById("nav-up-dropdown");
            console.log(dropdown);
            dropdown.style.display = "flex";
            dropdown.style.zIndex = "2";
            dropdown.style.top = "100%";



            // change the dropdown arrow direction
            let dd_arrow = document.getElementById("nav-up-dd-arrow");
            dd_arrow.style.transform = "rotate(180deg)";

            // change the visible attribute to true
            this.setAttribute('visible', 'true');

        // dropdown is shown, at the time of click
        } else if (this.getAttribute('visible') == "true") {
            // unshow the dropdown

            let dropdown = document.getElementById("nav-up-dropdown");
            console.log("dropdown" + dropdown);
            dropdown.style.zIndex = "-1";
            dropdown.style.top = "0%";
//            dropdown.style.display = "none";

            // change the dropdown arrow direction
            let dd_arrow = document.getElementById("nav-up-dd-arrow");
            dd_arrow.style.transform = "rotate(0deg)";
            // change the visible attribute to false
            this.setAttribute('visible', 'false');
        }

    });

  
    $('#search-bar-form').submit(function(){
        alert("mofo")
    });

    

});

/*
$("#sp-prev-arrow").click(function() {
    // get the 'rail' element
    let rails = document.querySelector(".sliding-promo-rails");
    let promo_wrapper = document.querySelector(".sliding-promo-wrapper");
    console.log(rails.children);
    console.log(rails.children.length);

    if (promo_carousel_index > 0) {
        promo_wrapper.style.width = "200%";
        rails.style.transition = "unset";
        rails.style.transform = `translateX(${-50}%)`;

        // show the previous promo. (promo is offscreen at this point)
        let prev_promo = rails.children[promo_carousel_index - 1];
        prev_promo.style.display = "flex";

        // decrement the carousel index
        promo_carousel_index--;

        setTimeout(()=>{
          rails.style.transition = "0.8s ease";
          rails.style.transform = "translateX(0%)";
          let next_promo = rails.children[promo_carousel_index + 1];
          // alert(next_promo.innerHTML);
          setTimeout(()=>{
            promo_wrapper.style.width = "100%";
            next_promo.style.display = "none";
          }, 10);
        }, 20);



        return

        setTimeout(function() {
            rails.style.transition = "unset";
            // unshow the current promo
            let current_promo = rails.children[promo_carousel_index + 1];
            current_promo.style.display = "none";

            promo_wrapper.style.width = "100%";
            rails.style.transform = "translateX(0%)";

            setTimeout(()=>{rails.style.transition = "1s ease"}, 100);

        },1000);
    }
});

$("#sp-next-arrow").click(function() {
    // get the 'rail' element
    let rails = document.querySelector(".sliding-promo-rails");
    let promo_wrapper = document.querySelector(".sliding-promo-wrapper");
    console.log(rails.children);
    console.log(rails.children.length);

    if (promo_carousel_index < rails.children.length-1) {
        promo_wrapper.style.width = "200%";

        // show the next promo. (promo is offscreen at this point)
        let next_promo = rails.children[promo_carousel_index + 1];
        next_promo.style.display = "flex";

        // increment the carousel index
        promo_carousel_index++;

        // move the carousel to show the next promo
        rails.style.transform = `translateX(${1 * -50}%)`;

        setTimeout(function() {
            rails.style.transition = "unset";
            // unshow the current promo
            let current_promo = rails.children[promo_carousel_index - 1];
            current_promo.style.display = "none";

            promo_wrapper.style.width = "100%";
            rails.style.transform = "translateX(0%)";

            setTimeout(()=>{rails.style.transition = "0.8s ease"}, 100);

        },1000);
    }

});
*/