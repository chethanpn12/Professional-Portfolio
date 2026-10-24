document.querySelectorAll("#year").forEach((node) => { node.textContent = new Date().getFullYear(); });
const printButton = document.getElementById("print-resume");
if (printButton) printButton.addEventListener("click", () => window.print());