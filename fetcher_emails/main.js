import { buscarEmails } from "./src/rotinas/fetch-emails.js";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

while (true) {
  console.log("Iniciando busca de emails...");
  const emails = await buscarEmails({
    email: "coderaceteste@gmail.com",
    senha: "scfh lgxp emaq owbw",
  });

  emails.forEach(async (email) => {
    const body = {
      from: email.from,
      subject: email.subject,
      text: email.text,
      to: email.to,
      date: email.date,
    };

    console.log("Enviando email:", body);

    await fetch("http://10.0.1.151:5000/recebendo_emails", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    }).catch((error) => {
      console.error("Erro ao enviar email:", error);
    });
  });
  console.log("Aguardando 60 segundos para a próxima busca...");

  sleep(6000);
}
