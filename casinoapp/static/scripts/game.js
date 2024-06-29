function changeSlideStyle(styles) {
  let keys = Object.keys(styles);
  let swiper_slides = document.querySelectorAll(".swiper-slide");
  
  keys.forEach(key=>{
      swiper_slides.forEach(slide=> {
      slide.style[key] = styles[key];
    });
  
  });

}

$(document).ready(function() {
  var swiper = new Swiper('.nigmajig', {
    loop: true,
    auto: true,
    
    effect: "coverflow",
    coverflowEffect: {
      depth: 50,
      modifier: 1,
      rotate: 20,
      scale: 1,
      slideShadows: true,
      stretch: 0,
    },
    grabCursor: true,
    centeredSlides: true,
    slidesPerView: "auto",

    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev'
    },

    pagination: {
      el: '.swiper-pagination'
    },
  });

  var selected_btn_genre = "";
  var current_game_name = "";
  
  changeSlideStyle({
    width: "40%",
    maxWidth: "100%",
    minWidth: "50%",
    borderRadius: "0.5rem",
  });

  function selectGenreBtn(clickedBtn) {   
    // adding the '.selected-btn' class to the selected button, removing from all other buttons
    let btn_wrapper = clickedBtn.parentElement;
    for (let btn of btn_wrapper.children) {
      // console.log(btn);
      btn.classList.remove("selected-btn");
    }
    clickedBtn.classList.add("selected-btn");

    // show the selected game page
    // let games_page = document.getElementById("games-page-holder");
    // let games_page_children = games_page.children;
    // let selected_page = document.getElementById(`${clickedBtn.id}-games`);
    // for (let i = 0; i < games_page_children.length; i++) {
    //   games_page_children[i].style.display = "none";
    // }
    // selected_page.style.display = "block";

  }
  
  $('.game-genre-btn').click(function() {
      selectGenreBtn(this);

      // prepare AJAX request
      let game_genre = this.getAttribute("dbval");
      selected_btn_genre = game_genre;
      current_game_name = game_genre; // for certain games, game_genre and game_name are the same i.e. Blackjack
      let dataToSend = JSON.stringify(game_genre);

      // send AJAX request
      ajaxDbTableRequest(DbTableJSONData(new_genre=true, game_genre=game_genre), true);    
  });

  function DbTableJSONData(new_genre=null, game_genre=null, game_name=null, min_bet=null, max_bet=null) {
    json_data = {
      "new_genre": new_genre,
      "game_genre": game_genre,
      "game_name": game_name,
      "min_bet": min_bet,
      "max_bet": max_bet,
    }

    return JSON.stringify(json_data);
  }
  
  function ajaxDbTableRequest(dataToSend, remakeDropdowns) {
    // send AJAX request
    $.ajax({
      method: "POST",
      url: "/select-game-genre",
      data: dataToSend,
      contentType: 'application/json',
      dataType: 'json',
      success: (result)=>{ajaxDbTableSuccessHandle(result, remakeDropdowns)},
      failure: ()=>{alert("FAILED")}
    });   
  }

  
  function ajaxDbTableSuccessHandle(result, remakeDropdowns) {
    // alert("JSON received");
    console.log(result);
    let gamesList = result["gamesList"];
    let gameFilterDropdowns = result["filterDropdown"];

    if (remakeDropdowns) {
      // clear existing dropdowns
      let dropdown_wrapper = document.getElementById("dropdown-wrapper");
      dropdown_wrapper.innerHTML = "";

      // make dropdowns
      for (let filter in gameFilterDropdowns) {
        // create dropdown element
        let filterSelect = document.createElement("select");
        filterSelect.id = filter + "-dropdown";

        let filterLabel = document.createElement("label");
        filterLabel.setAttribute('for', filterSelect.id);
        filterLabel.innerHTML = gameFilterDropdowns[filter].DropdownLabel + ":";

        // add handle for changing the dropdown value (prolly gonna make an ajax request to get new tables)
        filterSelect.addEventListener("change", (e)=>{
          // get all dropdowns
          dropdowns = document.querySelectorAll(".dropdown-wrapper select");
          console.log(dropdowns);
          bet_range = dropdowns[0].value.split(",");
          console.log(bet_range + "bet range");
          console.log(dropdowns.length + "length dropdown");

          let game_name_val = selected_btn_genre;
          // alert(selected_btn_genre);
    
          if (dropdowns.length >= 2) {
            // alert("GAMES HOW????");
            game_name_val = dropdowns[1].value;
            // alert(game_name_val);
          }

          // alert(game_name_val + "name val");
          // build data to send to backend
          frontend_data = DbTableJSONData(
            new_genre = false,
            game_genre = selected_btn_genre,
            game_name = game_name_val,
            min_bet = parseInt(bet_range[0]),
            max_bet = parseInt(bet_range[1])
          );

          console.log(frontend_data);

          // document.querySelector(".table-grid").innerHTML = "";

          // send AJAX request
          ajaxDbTableRequest(frontend_data, false);
        });

        // add each option for the dropdown element
        gameFilterDropdowns[filter].Options.forEach((option)=>{
          // create the option element
          let optionDOM = document.createElement("option");

          optionDOM.value = option;
          if (filter == "BetAmounts") {
            optionDOM.id = filter + ":" + `$${option[0]}-$${option[1]}`
            optionDOM.innerHTML = `$${option[0]}-$${option[1]}`;
          } else {
            optionDOM.id = filter + ":" + option;
            optionDOM.innerHTML = option;
          }        
          // style the option using class names

          // add the option to the dropdown element
          filterSelect.appendChild(optionDOM);
        });

        console.log(filterSelect);

        // add the dropdown element and its label to the parent wrapper
        dropdown_wrapper.appendChild(filterLabel);
        dropdown_wrapper.appendChild(filterSelect);
      }

    }
    
    let game_grid = document.querySelector(`#games-display .table-grid`);
    // clear existing tables
    game_grid.innerHTML = "";
    
    // display the available tables
    for (let i = 0; i < gamesList.length; i++) {
      let game_grid_item = document.createElement("a");
      game_grid_item.setAttribute("href", `${gamesList[i].gameName}/${gamesList[i].id}`);

      // make title
      let game_title = document.createElement("p");
      game_title.classList.add("table-grid-instance-title");
      game_title.innerHTML = gamesList[i].gameName;

      // bet amount
      let game_betamount = document.createElement("p");
      game_betamount.classList.add("btm-0");
      game_betamount.innerHTML = `$${gamesList[i].min_bet}-$${gamesList[i].max_bet}`

      // players
      let game_players = document.createElement("p");
      game_players.classList.add("btm-0");
      game_players.classList.add("right-0");
      game_players.innerHTML = `Players ${gamesList[i].no_players}/${gamesList[i].max_players}`

      game_grid_item.classList.add("grid-item");
      game_grid_item.style.backgroundColor = "blue";


      
      game_grid_item.appendChild(game_title);
      game_grid_item.appendChild(game_betamount);
      game_grid_item.appendChild(game_players);
      
      game_grid.appendChild(game_grid_item);
    }
  }
  
});
