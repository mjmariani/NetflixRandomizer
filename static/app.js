
// const instance = axios.create({
//     baseURL: 'https://api.themoviedb.org/3',
//     timeout: 1000,
//     headers: {'X-Custom-Header': 'foobar'}
//   });


// let genres = $(".genre-form").on( "submit", function( event ) {
//     event.preventDefault();
//     $( this ).serialize();
//   });

$( document ).ready(function() {
    console.log( "ready!" );
});

 $("#genre-form").on( "submit", async function( event ) {
     event.preventDefault();
    let forms = $(this).serializeArray();
    
    let genres, type;
    [genres, type] = splitGenresAndTypes(forms);
    // console.log(`genres =  ${genres}`);

    let response = await video_type_router(genres, type);
    console.log(response);
    let flag = true;
    $.getScript("static/index.js", function(response){
        tinder_wheel(response);
    });
    

   });

   let card_removed = 0;
// $(".tinder--cards").


 function splitGenresAndTypes (forms){
    let genres = [];
    let type = [];

    // form_data.forEach((element) => {
    //     if(element.name=="genres"){
    //         genres.push(element.value);
    //     }
    //     if(element.name=="type"){
    //         type.push(element.value);
    //     }
    // });

    for(let index in forms){


   if(forms[index].name === "genres"){
         genres.push(forms[index].value);
    }

    if(forms[index].name === "video_type"){
         type.push(forms[index].value);

    }
 }
return [genres, type];

 }




async function video_type_router(genres, type){
if(type[0]==="Movies"){
    return await getMovies(genres, type);
}
if(type[0]==="TV_Show"){
    return await getTVShows(genres, type);
}

}

async function getMovies(genres, type){
    let genres_string = genres.toString();
    console.log("in get movie");
 return await axios.get('https://api.themoviedb.org/3/discover/movie', {
    params: {
      api_key: '35a466991fbef8b9209345a5bdfbf733',
        sort_by: 'popularity.desc',
        
        include_video: 'True',
        language: 'en-US',
        with_genres: genres_string



    }
  })
  .then((response) =>{
    
    return response;
})
  .catch((error) => {
    console.log(error);
    return error;
  });}


