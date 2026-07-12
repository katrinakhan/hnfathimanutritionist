const videoPlayer = document.getElementById('videoPlayer');
const playButton = document.querySelector('.play-button');

if (videoPlayer && playButton) {
    playButton.addEventListener('click', function () {
        videoPlayer.play();
        this.style.display = 'none';
    });

    videoPlayer.addEventListener('play', function () {
        playButton.style.display = 'none';
    });

    videoPlayer.addEventListener('pause', function () {
        playButton.style.display = 'block';
    });

    videoPlayer.addEventListener('ended', function () {
        playButton.style.display = 'block';
    });
}
