let form = document.querySelector("form");
let urlInput = document.getElementById("url");
const loadAnimation = document.querySelector(".load");

let sendRequest = async (endpoint, payload, method = "POST", headers = {}) => {
    let requestOptions = {
        method: method,
        body: payload,
    };

    const res = await fetch(endpoint, requestOptions);
    if (res.ok) {
        json = await res.json();
        return json;
    } else {
        console.error("Error sending the request");
    }
};

function download() {
    let parent = this.parentElement.parentElement;
    let video_url = parent.getAttribute("video_url");
    let downloadType = document.querySelector(
        "input[name='res']:checked"
    ).value;
    let anchor = document.createElement("a");
    if (downloadType === "mp3") {
        anchor.href = `${window.location.origin}/download-audio?url=${video_url}`;
    } else {
        anchor.href = `${window.location.origin}/download-video?url=${video_url}&res=${downloadType}`;
    }
    anchor.target = "_blank";
    anchor.click();
}

form.addEventListener("submit", (event) => {
    event.preventDefault();
    loadAnimation.style.display = "flex";

    formData = new FormData(form);
    sendRequest("/video-info", formData).then((json) => {
        let existingVideo = document.querySelector(".video");
        if (existingVideo) existingVideo.parentNode.removeChild(existingVideo);
        let contentDiv = document.querySelector(".content");
        let div = document.createElement("div");
        let img = document.createElement("img");
        let videoInfo = document.createElement("span");
        let downloadButton = document.createElement("button");
        let resolutions = [];
        for (let i of json.resolutions) {
            resolutions.push(`<input id="${i}" type="radio" name ="res" value= "${i}">
                              <label for="${i}">${i}</label>`);
        }
        div.className = "video";
        img.setAttribute("src", json.thumbnail);
        videoInfo.innerHTML = `
        <a href= "${urlInput.value}"><p>${json.title}</p></a>
        <div class="resolutions">
            ${resolutions.join("\n")}
        </div>
        `;
        downloadButton.innerText = "Download";
        downloadButton.onclick = download;
        downloadButton.className = "download";
        videoInfo.appendChild(downloadButton);
        div.appendChild(img);
        div.appendChild(videoInfo);
        contentDiv.appendChild(div);
        div.setAttribute("video_url", urlInput.value);
        urlInput.value = "";
        loadAnimation.style.display = "none";
    });
});
