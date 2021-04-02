//to delete queue elements on details.html page
document.querySelectorAll('#delete-button').addEventListener("click", handleClick, false);

async function handleClick(event) {
        event.preventDefault();
        let userId = $('#delete-button').data("userId");
        let videoId = $('#delete-button').data("itemId");
        await axios.delete(`http://127.0.0.1:5000/users/${userId}`, {
params: {
  id = videoId,
    



}
})
.then((response) =>{

return response;
})
.catch((error) => {
console.log(error);
return error;
});

        
        removeItem(event.target.parentNode);
    
}