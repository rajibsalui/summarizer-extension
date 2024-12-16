chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "summarize") {
    const url = `http://127.0.0.1:8000/summarize?url=${encodeURIComponent(request.url)}`;
    chrome.tabs.create({ url });
  }
});