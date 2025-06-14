import { buscarEmails } from "./src/rotinas/fetch-emails.js";

const TEMPLATE =
  "Abaixo está o conteudo de um email, verifique se há possiveis reunioes ou eventos que possam ser agendados. Tarefas e atividades, entregas, trabalhos também devem ser considerados " +
  "Se houver, responda com algo tipo '2025-07-21T14:00:00-03:00 Jogar bola com Miguel', se não responda com 'não há eventos agendados', nao responda nada alem disso. " +
  "considere a data de hj: " +
  new Date().toDateString() +
  "Se houver elementos como 'outra reuniao' ou 'outro agendamento', considere que é uma reunião já agendada e deve ser criada uma nova reunião com nome tipo 'reuniao com davi 2'. segue o email: ";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

while (true) {
  console.log("🕵️ Iniciando busca de emails...");
  const emails = await buscarEmails({
    email: "coderaceteste@gmail.com",
    senha: "scfh lgxp emaq owbw",
  });

  for (const email of emails) {
    const body = {
      from: email.from,
      subject: email.subject,
      text: email.text,
      to: email.to,
      date: email.date,
    };

    console.log("📨 Email recebido:", body.subject);

    const response = await fetch("http://10.0.1.195:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer sk-7aTQ9NpzV3w2uE4LmRbJxYcAq6ZHtXfG",
      },
      body: JSON.stringify({
        prompt:
          TEMPLATE +
          "de: " +
          body.from +
          " para: " +
          body.to +
          " assunto: " +
          body.subject +
          " conteudo: " +
          body.text,
      }),
    }).catch((error) => {
      console.error("❌ Erro ao enviar prompt para o servidor de chat:", error);
    });

    if (!response) {
      console.error("❌ Falha ao obter resposta do servidor de chat.");
      continue;
    }

    let respostaAgendamento;
    try {
      respostaAgendamento = await response.json();
    } catch (e) {
      console.error("❌ Erro ao interpretar JSON do servidor de chat:", e);
      continue;
    }

    console.log("🤖 Resposta do servidor:", respostaAgendamento);

    const startDateTime =
      respostaAgendamento.response?.split(" ")[0] ||
      "2025-01-01T00:00:00-03:00";
    const description =
      respostaAgendamento.response || "Não há eventos agendados";

    const respostaCalendario = await fetch(
      "http://10.0.1.117:8080/api/events",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          startDateTime,
          summary: description,
          location: "Remoto",
          description,
          endDateTime: startDateTime,
        }),
      }
    ).catch((error) => {
      console.error("❌ Erro ao enviar resposta para o calendário:", error);
    });

    if (respostaCalendario) {
      console.log("📅 Evento enviado ao calendário com sucesso.");
    }
  }

  console.log("⏳ Aguardando 60 segundos para a próxima busca...");
  await sleep(60000);
}
