/*Parts of Code Downloaded from https://www.codeseek.co/RobVermeer/tinder-swipe-cards-japZpY */
'use strict';

//const { debug } = require("node:console");



let page = 1;

async function tinder_wheel(response, genres, type) {
  try {
    console.log(response)
    let tinderContainer = document.querySelector('.tinder');
    let allCards = document.querySelectorAll('.tinder--card');
    // let nope = document.getElementById('nope');
    // let love = document.getElementById('love');
    let newCardCount = 0;
    let id = 1;
    let count = 0;
    let data;
    let nopeListener = await createButtonListener(false);

    let loveListener = await createButtonListener(true);

    document.getElementById('nope').addEventListener('click', nopeListener);

    document.getElementById('love').addEventListener('click', loveListener);

    async function initCards(card, index) {
      if (newCardCount > 0) {
        await refreshCards();

        let tinderContainer = document.querySelector('.tinder');
        let allCards = document.querySelectorAll('.tinder--card');
        let nope = document.getElementById('nope');
        let love = document.getElementById('love');
        let newCard = document.getElementById(id);
        addAction(newCard);
        addData(newCard);
        newCardCount -= 1;
        id += 1;
        if (id == 15) {
          page++;
          response = await getNewPage(genres, type);
        }
      }
      let newCards = document.querySelectorAll('.tinder--card:not(.removed)');
      newCards.forEach(async function (card, index) {
        card.style.zIndex = allCards.length - index;
        card.style.transform = 'scale(' + (20 - index) / 20 + ') translateY(-' + 30 * index + 'px)';
        card.style.opacity = (10 - index) / 10;
      });
      tinderContainer.classList.add('loaded');
    }
    await initCards();
    await addNewData();
    allCards.forEach(addAction);

    function addAction(el) {

      var hammertime = new Hammer(el);

      hammertime.on('pan', function (event) {
        el.classList.add('moving');
      });

      hammertime.on('pan', function (event) {
        if (event.deltaX === 0) return;
        if (event.center.x === 0 && event.center.y === 0) return;

        tinderContainer.classList.toggle('tinder_love', event.deltaX > 0);

        tinderContainer.classList.toggle('tinder_nope', event.deltaX < 0);


        var xMulti = event.deltaX * 0.03;
        var yMulti = event.deltaY / 80;
        var rotate = xMulti * yMulti;

        event.target.style.transform = 'translate(' + event.deltaX + 'px, ' + event.deltaY + 'px) rotate(' + rotate + 'deg)';
      });

      hammertime.on('panend', async function (event) {
        el.classList.remove('moving');
        tinderContainer.classList.remove('tinder_love');
        tinderContainer.classList.remove('tinder_nope');

        var moveOutWidth = document.body.clientWidth;
        var keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;

        event.target.classList.toggle('removed', !keep);
        event.target.classList.toggle(`liked`, !keep);


        if (keep) {
          event.target.style.transform = '';
        } else {
          var endX = Math.max(Math.abs(event.velocityX) * moveOutWidth, moveOutWidth);
          var toX = event.deltaX > 0 ? endX : -endX;
          var endY = Math.abs(event.velocityY) * moveOutWidth;
          var toY = event.deltaY > 0 ? endY : -endY;
          var xMulti = event.deltaX * 0.03;
          var yMulti = event.deltaY / 80;
          var rotate = xMulti * yMulti;

          event.target.style.transform = 'translate(' + toX + 'px, ' + (toY + event.deltaY) + 'px) rotate(' + rotate + 'deg)';
          newCardCount += 1;

          if (event.target.classList.contains('liked')) {
            await postLikeToDB(event.target);
          }
          await initCards();

        }
      });
    }


    async function createButtonListener(love) {
      return async function (event) {
        let cards = document.querySelectorAll('.tinder--card:not(.removed)');

        let moveOutWidth = document.body.clientWidth * 1.5;

        if (!cards.length) return false;

        let card = cards[0];

        card.classList.add('removed');

        if (love) {
          card.style.transform = 'translate(' + moveOutWidth + 'px, -100px) rotate(-30deg)';
          card.className += ` liked`;
          await postLikeToDB(card);



        } else {
          card.style.transform = 'translate(-' + moveOutWidth + 'px, -100px) rotate(30deg)';
        }

        newCardCount = 1;
        await initCards();
      }

    }



    async function refreshCards() {



      let htmlContent = `<div class="tinder--card" id=${id}>` +
        '<img src="../static/images/AdobeStock_360066662_Preview_Editorial_Use_Only.jpeg">' +
        '<div data-toggle="modal" data-target="#exampleModal" class="card-info"><h3></h3></div>' +
        '<p></p>' +
        '</div>';

      $(".tinder--cards").append(htmlContent);


    }

    async function addNewData() {
      count = 0;
      let newCards = document.querySelectorAll('.tinder--card');

      let newCardsArray = Array.prototype.slice.call(newCards);

      newCardsArray.forEach(async function (card, count) {

        let img = await response.data.results[count].poster_path;

        let data = await response.data.results[count]

        card.childNodes[1].src = `https://image.tmdb.org/t/p/w500${img}`;
        if (type == "Movies") {
          card.querySelector('h3').innerText = data.title;
        } else {

          card.querySelector('h3').innerText = data.name;
        }
        if (type == "Movies") {
          let trailer = await axios.get(`https://api.themoviedb.org/3/movie/${data.id}/videos`, {
            params: {
              api_key: '35a466991fbef8b9209345a5bdfbf733',
            }
          })
        }
        card.onclick = function () {
          document.querySelector('.description').innerHTML = "";
          document.querySelector('.description').append("Description: " + data.overview);
          //  document.querySelector('.trailer').innerHTML = "";
          //  document.querySelector('.trailer').append("Trailer: " + trailer.results[0].site);
        }

        count++;

      });
    }

    async function postLikeToDB(card) {

      try {
        await axios({
          method: 'post',
          url: `${window.location.protocol}//${window.location.hostname}/show`,
          data: {
            'like': 'True',
            'name': `${card.innerText}`,
            'id': `${response.data.results[count].id}`,
            'type': `${type}`
          }
        })
      } catch (error) {
        console.log(error);
      };
    }


    async function addData(card) {

      let img = await response.data.results[count].poster_path;
      let data = await response.data.results[count]

      //console.log(data);
      card.childNodes[0].src = `https://image.tmdb.org/t/p/w500${img}`;
      card.childNodes[1].innerText = data.original_title;
      card.onclick = function () {
        document.querySelector('.description').innerHTML = "";
        document.querySelector('.description').append("Description: " + data.overview);
        document.querySelector('.trailer').innerHTML = "";
      }
      count++;
    }
    //return true;
  } catch (error) {
    console.log(error);
  }
}

async function getNewPage(genres, type) {
  response = await video_type_router(genres, type);

  return response;
}


async function video_type_router(genres, type) {
  if (type[0] === "Movies") {
    return await getMovies(genres, type);
  }
  if (type[0] === "TV_Show") {
    return await getTVShows(genres, type);
  }

}

async function getMovies(genres, type) {
  let genres_string = genres.toString();

  console.log("in get movie");
  if (type == "Movies") {
    return await axios.get('https://api.themoviedb.org/3/discover/movie', {
        params: {
          api_key: '35a466991fbef8b9209345a5bdfbf733',
          sort_by: 'popularity.desc',

          include_video: 'True',
          language: 'en-US',
          with_genres: genres_string,

          page: `${page}`


        }
      })
      .then((response) => {

        return response;
      })
      .catch((error) => {
        console.log(error);
        return error;
      });
  } else {

    return await axios.get('https://api.themoviedb.org/3/discover/tv', {
        params: {
          api_key: '35a466991fbef8b9209345a5bdfbf733',
          sort_by: 'popularity.desc',

          include_video: 'True',
          language: 'en-US',
          with_genres: genres_string,

          page: `${page}`


        }
      })
      .then((response) => {

        return response;
      })
      .catch((error) => {
        console.log(error);
        return error;
      });


  }


  async function getTVShows(genres, type) {
    let genres_string = genres.toString();

    console.log("in get movie");
    return await axios.get('https://api.themoviedb.org/3/discover/tv', {
        params: {
          api_key: '35a466991fbef8b9209345a5bdfbf733',
          sort_by: 'popularity.desc',

          include_video: 'True',
          language: 'en-US',
          with_genres: genres_string,

        }

      })
      .then((response) => {

        return response;
      })
      .catch((error) => {
        console.log(error);
        return error;
      });
  }
}