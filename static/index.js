/*Downloaded from https://www.codeseek.co/RobVermeer/tinder-swipe-cards-japZpY */
'use strict';

function tinder_wheel(response){
  let tinderContainer = document.querySelector('.tinder');
  let allCards = document.querySelectorAll('.tinder--card');
  let nope = document.getElementById('nope');
  let love = document.getElementById('love');
  let newCardCount = 0;
  let id = 1;
  function initCards(card, index) {
    if(newCardCount > 0){
    refreshCards();
    let tinderContainer = document.querySelector('.tinder');
    let allCards = document.querySelectorAll('.tinder--card');
    let nope = document.getElementById('nope');
    let love = document.getElementById('love');
    let newCard = document.getElementById(id);
    addAction(newCard);
    newCardCount -= 1;
    id += 1;
  }
    let newCards = document.querySelectorAll('.tinder--card:not(.removed)');
  
    newCards.forEach(function (card, index) {
      card.style.zIndex = allCards.length - index;
      card.style.transform = 'scale(' + (20 - index) / 20 + ') translateY(-' + 30 * index + 'px)';
      card.style.opacity = (10 - index) / 10;
    });
    
    tinderContainer.classList.add('loaded');
    
  }
  
  initCards();
  
  allCards.forEach(addAction);
  function addAction (el) {
    
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
  
    hammertime.on('panend', function (event) {
      el.classList.remove('moving');
      tinderContainer.classList.remove('tinder_love');
      tinderContainer.classList.remove('tinder_nope');
  
      var moveOutWidth = document.body.clientWidth;
      var keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;
  
      event.target.classList.toggle('removed', !keep);
  
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
        initCards();
        
      }
    });
  }
  
  
  function createButtonListener(love) {
    return function (event) {
      let cards = document.querySelectorAll('.tinder--card:not(.removed)');
      let moveOutWidth = document.body.clientWidth * 1.5;
  
      if (!cards.length) return false;
  
      let card = cards[0];
  
      card.classList.add('removed');
  
      if (love) {
        card.style.transform = 'translate(' + moveOutWidth + 'px, -100px) rotate(-30deg)';
      } else {
        card.style.transform = 'translate(-' + moveOutWidth + 'px, -100px) rotate(30deg)';
      }
  
      newCardCount = 1;
      initCards();
      
      event.preventDefault();
    };
  }
  
  let nopeListener = createButtonListener(false);
  let loveListener = createButtonListener(true);
  
  nope.addEventListener('click', nopeListener);
  love.addEventListener('click', loveListener);

  function refreshCards(){
    
      
        
      let htmlContent = `<div class="tinder--card" id=${id}>` +
      '<img src="https://placeimg.com/600/300/people">' +
      '<h3>Demo card 1</h3>' +
      '<p>This is a demo for Tinder like swipe cards</p>' +
      '</div>';
  
      $(".tinder--cards").append(htmlContent);

      
      
  
  }

}




