function speakText(index) {
  if (!window.STEPS || !window.STEPS[index]) return;
  speak(window.STEPS[index]);
}

function speakAll() {
  if (!window.STEPS) return;
  let i = 0;
  function next() {
    if (i >= window.STEPS.length) return;
    speak(window.STEPS[i], () => {
      i++;
      setTimeout(next, 300); // small gap
    });
  }
  next();
}

function speak(text, cb) {
  if (!('speechSynthesis' in window)) {
    alert("Speech synthesis not supported in this browser.");
    if (cb) cb();
    return;
  }
  const msg = new SpeechSynthesisUtterance(text);
  msg.lang = 'en-US';
  msg.rate = 0.95;
  msg.onend = function() { if (cb) cb(); };
  window.speechSynthesis.cancel(); // stop previous
  window.speechSynthesis.speak(msg);
}
