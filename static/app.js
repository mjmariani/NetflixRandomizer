
const instance = axios.create({
    baseURL: 'https://api.themoviedb.org/3',
    timeout: 1000,
    headers: {'X-Custom-Header': 'foobar'}
  });


// let genres = $(".genre-form").on( "submit", function( event ) {
//     event.preventDefault();
//     $( this ).serialize();
//   });

$( document ).ready(function() {
    console.log( "ready!" );
});

 let genres = $("#genre-form").on( "submit", function( event ) {
     event.preventDefault();
     

   }).serializeArray();

function getMovies(genres, type){
axios.get('/authentication/guest_session/new', {
    params: {
      api_key: '35a466991fbef8b9209345a5bdfbf733',
        sort_by: 'popularity.desc',
        include_adult: 'false',
        include_video: 'true',
        with_genres: ''

    }
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  })
  .then(function () {
    // always executed
  });}


