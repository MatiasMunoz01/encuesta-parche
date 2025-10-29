document.getElementById("encuestaForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    edad: document.querySelector('input[name="edad"]').value,
    frecuencia: document.querySelector('input[name="frecuencia"]').value,
    companeros: document.querySelector('input[name="companeros"]').value,
    bebida_favorita: document.querySelector('input[name="bebida_favorita"]').value,
  };

  const res = await fetch("/enviar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const result = await res.json();
  document.getElementById("resultado").innerText = result.message || result.error;
});
