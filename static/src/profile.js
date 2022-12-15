'use strict'; 

console.log('Connected!')

var audio = new Audio('https://assets.ctfassets.net/v3n26e09qg2r/5m3SPslo3HRy1DGTnGgpwb/a5c12d0e6285e4a4cb2d1cc5d266dc21/Breath.mp3') // from Headspace downloadable audio 
///////////////////////////////////////////

const five = document.getElementById('five')

five.addEventListener('click', function () {
    var timeoutHandle;
        function countdown(minutes, seconds) {
            function tick() {
                var counter = document.getElementById("timer-result");
                counter.innerHTML = 
                minutes.toString() + ":" + (seconds < 10 ? "0" : "") + String(seconds);
                seconds-=1;
                if (seconds < 0 && minutes == 0) {
                    audio.play();
                } else if (seconds >= 0) {
                    timeoutHandle = setTimeout(tick, 1000);
                } else { 
                    if (minutes >= 1) {
                        setTimeout(function () {
                        countdown(minutes - 1, 59);
                        }, 1000);
                    }
                }
            }
            tick();
        }
        countdown(5, 0);
});


// TODO: Figure out how to not repeat startMeditation function for both 5 and 10 min timer


function startMeditation(evt) {
    evt.preventDefault();
    const length = document.getElementById('five').value;

    fetch('/meditation', {
        method: 'POST',
        body: JSON.stringify({length}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((response) => response.json())
    .then((responseJson) => {
        document.getElementById('meditation-data').innerText = JSON.stringify(responseJson)
    });
};
document.getElementById('five').addEventListener('click', startMeditation);


const ten = document.getElementById('ten')

ten.addEventListener('click', function () {
    var timeoutHandle;
        function countdown(minutes, seconds) {
            function tick() {
                var counter = document.getElementById("timer-result");
                counter.innerHTML =
                minutes.toString() + ":" + (seconds < 10 ? "0" : "") + String(seconds);
                seconds-=1;
                if (seconds < 0 && minutes == 0) {
                    audio.play();
                } else if (seconds >= 0) {
                    timeoutHandle = setTimeout(tick, 1000);
                } else {
                    if (minutes >= 1) {
                        setTimeout(function () {
                            countdown(minutes - 1, 59);
                        }, 1000);
                    }
                }
            }
            tick();
        }
        countdown(10, 0);
});

function startMeditation(evt) {
    evt.preventDefault();
    const length = document.getElementById('ten').value;

    fetch('/meditation', {
        method: 'POST',
        body: JSON.stringify({length}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((response) => response.json())
    .then((responseJson) => {
        document.getElementById('meditation-data').innerText = JSON.stringify(responseJson)
    });
};
document.getElementById('ten').addEventListener('click', startMeditation);
/////////////////////////////////////////////////////

// This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player1, player2, player3, player4;
    function onYouTubeIframeAPIReady() {

    var ctrlq1 = document.getElementById("youtube-audio1");
    ctrlq1.innerHTML = '<img id="youtube-icon1" src=""/><div id="youtube-player1"></div>';
    ctrlq1.style.cssText = 'width:150px;margin:2em auto;cursor:pointer;cursor:hand;display:none';
    ctrlq1.onclick = toggleAudio1;

    player1 = new YT.Player('youtube-player1', {
        height: '0',
        width: '0',
        videoId: ctrlq1.dataset.video,
        playerVars: {
        autoplay: ctrlq1.dataset.autoplay,
        loop: ctrlq1.dataset.loop,
        },
        events: {
        'onReady': onPlayerReady1,
        'onStateChange': onPlayerStateChange1 
        } 
    });

    var ctrlq2 = document.getElementById("youtube-audio2");
    ctrlq2.innerHTML = '<img id="youtube-icon2" src=""/><div id="youtube-player2"></div>';
    ctrlq2.style.cssText = 'width:150px;margin:2em auto;cursor:pointer;cursor:hand;display:none';
    ctrlq2.onclick = toggleAudio2;

    player2 = new YT.Player('youtube-player2', {
        height: '0',
        width: '0',
        videoId: ctrlq2.dataset.video,
        playerVars: {
        autoplay: ctrlq2.dataset.autoplay,
        loop: ctrlq2.dataset.loop,
        },
        events: {
        'onReady': onPlayerReady2,
        'onStateChange': onPlayerStateChange2
        } 
    });

    var ctrlq3 = document.getElementById("youtube-audio3");
    ctrlq3.innerHTML = '<img id="youtube-icon3" src=""/><div id="youtube-player3"></div>';
    ctrlq3.style.cssText = 'width:150px;margin:2em auto;cursor:pointer;cursor:hand;display:none';
    ctrlq3.onclick = toggleAudio3;

    player3 = new YT.Player('youtube-player3', {
        height: '0',
        width: '0',
        videoId: ctrlq3.dataset.video,
        playerVars: {
        autoplay: ctrlq3.dataset.autoplay,
        loop: ctrlq3.dataset.loop,
        },
        events: {
        'onReady': onPlayerReady3,
        'onStateChange': onPlayerStateChange3 
        } 
    });

    var ctrlq4 = document.getElementById("youtube-audio4");
    ctrlq4.innerHTML = '<img id="youtube-icon4" src=""/><div id="youtube-player4"></div>';
    ctrlq4.style.cssText = 'width:150px;margin:2em auto;cursor:pointer;cursor:hand;display:none';
    ctrlq4.onclick = toggleAudio4;

    player4 = new YT.Player('youtube-player4', {
        height: '0',
        width: '0',
        videoId: ctrlq4.dataset.video,
        playerVars: {
        autoplay: ctrlq4.dataset.autoplay,
        loop: ctrlq4.dataset.loop,
        },
        events: {
        'onReady': onPlayerReady4,
        'onStateChange': onPlayerStateChange4 
        } 
    });
    } 
// Toggles the play buttons and audio 
    function togglePlayButton1(play) {    
    document.getElementById("youtube-icon1").src = play ? "https://i.imgur.com/IDzX9gL.png" : "https://i.imgur.com/quyUPXN.png";
    }

    function toggleAudio1() {
    if ( player1.getPlayerState() == 1 || player1.getPlayerState() == 3 ) {
        player1.pauseVideo(); 
        togglePlayButton1(false);
    } else {
        player1.playVideo(); 
        togglePlayButton1(true);
    } 
    } 

    function togglePlayButton2(play) {    
    document.getElementById("youtube-icon2").src = play ? "https://i.imgur.com/IDzX9gL.png" : "https://i.imgur.com/quyUPXN.png";
    }

    function toggleAudio2() {
    if ( player2.getPlayerState() == 1 || player2.getPlayerState() == 3 ) {
        player2.pauseVideo(); 
        togglePlayButton2(false);
    } else {
        player2.playVideo(); 
        togglePlayButton2(true);
    } 
    } 

    function togglePlayButton3(play) {    
    document.getElementById("youtube-icon3").src = play ? "https://i.imgur.com/IDzX9gL.png" : "https://i.imgur.com/quyUPXN.png";
    }

    function toggleAudio3() {
    if ( player3.getPlayerState() == 1 || player3.getPlayerState() == 3 ) {
        player3.pauseVideo(); 
        togglePlayButton3(false);
    } else {
        player3.playVideo(); 
        togglePlayButton3(true);
    } 
    } 

    function togglePlayButton4(play) {    
    document.getElementById("youtube-icon4").src = play ? "https://i.imgur.com/IDzX9gL.png" : "https://i.imgur.com/quyUPXN.png";
    }

    function toggleAudio4() {
    if ( player4.getPlayerState() == 1 || player4.getPlayerState() == 3 ) {
        player4.pauseVideo(); 
        togglePlayButton4(false);
    } else {
        player4.playVideo(); 
        togglePlayButton4(true);
    } 
    } 
    // API will call this function when video player is ready
    function onPlayerReady1(event) {
    player1.setPlaybackQuality("small");
    document.getElementById("youtube-audio1").style.display = "block";
    togglePlayButton1(player1.getPlayerState() !== 5);
    }
    // API calls this function when the player's state changes - indicates that when playing a video (state = 1) the player should play 
    function onPlayerStateChange1(event) {
    if (event.data === 0) {
        togglePlayButton1(false); 
    }
    }

    function onPlayerReady2(event) {
    player2.setPlaybackQuality("small");
    document.getElementById("youtube-audio2").style.display = "block";
    togglePlayButton2(player2.getPlayerState() !== 5);
    }

    function onPlayerStateChange2(event) {
    if (event.data === 0) {
        togglePlayButton2(false); 
    }
    }

    function onPlayerReady3(event) {
    player3.setPlaybackQuality("small");
    document.getElementById("youtube-audio3").style.display = "block";
    togglePlayButton3(player3.getPlayerState() !== 5);
    }

    function onPlayerStateChange3(event) {
    if (event.data === 0) {
        togglePlayButton3(false); 
    }
    }

    function onPlayerReady4(event) {
    player4.setPlaybackQuality("small");
    document.getElementById("youtube-audio4").style.display = "block";
    togglePlayButton4(player4.getPlayerState() !== 5);
    }

    function onPlayerStateChange4(event) {
    if (event.data === 0) {
        togglePlayButton4(false); 
    }
    }
/////////////////////////////////////////////////////