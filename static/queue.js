//to delete queue elements on details.html page
let element = document.querySelectorAll('#delete-button')
element[0].addEventListener("click", handleClick);

async function handleClick(event) {
        event.preventDefault();
        let userId = $('#delete-button').data("userId");
        let videoId = $('#delete-button').data("itemId");
        event.target.parentNode.remove();
        await axios.delete(`${window.location.protocol}//${window.location.hostname}/users/${userId}`, {
params: {
'id': `${videoId}`,
}})
.then((response) =>{

return response;
})
.catch((error) => {
console.log(error);
return error;
});

        

    
}