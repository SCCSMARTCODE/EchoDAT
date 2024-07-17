document.addEventListener('DOMContentLoaded', function() {
    const audio = document.getElementById('audio');
    const playPauseButton = document.getElementById('play-pause');
    const currentTimeElem = document.getElementById('current-time');
    const durationElem = document.getElementById('duration');
    const seekBar = document.getElementById('seek-bar');
    const muteButton = document.getElementById('mute');
    const volumeBar = document.getElementById('volume-bar');

    audio.addEventListener('loadedmetadata', function() {
        console.log('Audio loaded');
        durationElem.textContent = formatTime(audio.duration);
    });

    audio.addEventListener('timeupdate', function() {
        const currentTime = formatTime(audio.currentTime);
        currentTimeElem.textContent = currentTime;
        seekBar.value = (audio.currentTime / audio.duration) * 100;
    });

    audio.addEventListener('play', function() {
        console.log('Audio started playing');
        playPauseButton.textContent = 'Pause';
    });

    audio.addEventListener('pause', function() {
        console.log('Audio paused');
        playPauseButton.textContent = 'Play';
    });

    audio.addEventListener('ended', function() {
        console.log('Audio ended');
        playPauseButton.textContent = 'Play';
    });

    audio.addEventListener('error', function(e) {
        console.error('Audio error', e);
        const error = e.target.error;
        switch(error.code) {
            case error.MEDIA_ERR_ABORTED:
                console.error('You aborted the audio playback.');
                break;
            case error.MEDIA_ERR_NETWORK:
                console.error('A network error caused the audio download to fail.');
                break;
            case error.MEDIA_ERR_DECODE:
                console.error('The audio playback was aborted due to a corruption problem or because the video used features your browser did not support.');
                break;
            case error.MEDIA_ERR_SRC_NOT_SUPPORTED:
                console.error('The audio could not be loaded, either because the server or network failed or because the format is not supported.');
                break;
            default:
                console.error('An unknown error occurred.');
                break;
        }
    });

    playPauseButton.addEventListener('click', function() {
        if (audio.paused) {
            audio.play();
        } else {
            audio.pause();
        }
    });

    seekBar.addEventListener('input', function() {
        audio.currentTime = (seekBar.value / 100) * audio.duration;
    });

    muteButton.addEventListener('click', function() {
        audio.muted = !audio.muted;
        muteButton.textContent = audio.muted ? 'Unmute' : 'Mute';
    });

    volumeBar.addEventListener('input', function() {
        audio.volume = volumeBar.value;
    });

    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        seconds = Math.floor(seconds % 60);
        return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }
});

    window.addEventListener('scroll', function() {
        var header = document.getElementById('header');
        if (window.pageYOffset > 0) {
            header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

    window.addEventListener('scroll', function() {
        var logo = document.querySelector('.logo img');
        if (window.pageYOffset > 0) {
            logo.src = 'img/logo11.png'; // Change to the white logo
    } else {
        logo.src = 'img/logo12.png'; // Change back to the green logo
    }
});


