# How i Get All Followers and Following from Instagram

## Step by step
> If you want to see the tutorial in video, please see [this video](docs/video/recording.webm)

1. Open your Instagram profile
2. Open the followers or following list
3. Open the browser console (F12)
4. Paste the code below [Show all users loaded every 2 seconds](InstagramScripts.md#show-all-users-loaded-every-2-seconds)
5. Press enter
6. scroll down to load all users
7. When number of elements found is equal to the number of followers or following
8. Run the second code to download all users loaded [Download all users loaded](InstagramScripts.md#download-all-users-loaded)

# Scripts

## Show all users loaded every 2 seconds

```javascript
function countElements() {
  const elements = document.getElementsByClassName("x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3");
  console.log(`Number of elements found: ${elements.length}`);
}

setInterval(countElements, 2000);
```

## Download all users loaded

```javascript
function downloadFile(data, filename, type) {
  const file = new Blob([data], { type: type });
  const a = document.createElement("a");
  const url = URL.createObjectURL(file);
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  setTimeout(function () {
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }, 0);
}

function getAndDownloadValues(filename = "element_values") {
  const elements = document.getElementsByClassName("_ap3a _aaco _aacw _aacx _aad7 _aade");
  let values = "";

  for (let i = 0; i < elements.length; i++) {
    values += elements[i].innerText + "\n";
  }

  downloadFile(values, filename + ".txt", "text/plain");
}

getAndDownloadValues();


```