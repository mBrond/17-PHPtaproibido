import Imap from "imap";
import { simpleParser } from "mailparser";

export function buscarEmails({ email, senha }) {
  return new Promise((resolve, reject) => {
    const imap = new Imap({
      user: email,
      password: senha,
      host: "imap.gmail.com",
      port: 993,
      tls: true,
      tlsOptions: {
        rejectUnauthorized: false,
      },
    });

    function openInbox(cb) {
      imap.openBox("[Gmail]/All Mail", true, cb);
    }

    imap.once("ready", () => {
      openInbox((err, box) => {
        if (err) return reject(err);

        imap.search(["UNSEEN"], (err, results) => {
          if (err || !results.length) {
            imap.end();
            return resolve([]);
          }
          const sortedResults = results.sort((a, b) => b - a);
          const fetch = imap.fetch(sortedResults.slice(0, 5), {
            bodies: "",
            markSeen: false,
          });

          const parsePromises = [];

          fetch.on("message", (msg) => {
            const promise = new Promise((res, rej) => {
              msg.on("body", (stream) => {
                simpleParser(stream)
                  .then((parsed) => {
                    res({
                      subject: parsed.subject,
                      from: parsed.from.text,
                      to: parsed.to.text,
                      date: parsed.date,
                      text: parsed.text,
                    });
                  })
                  .catch(rej);
              });
            });

            parsePromises.push(promise);
          });

          fetch.once("end", async () => {
            try {
              const emails = await Promise.all(parsePromises);
              imap.end();
              resolve(emails);
            } catch (e) {
              reject(e);
            }
          });
        });
      });
    });

    imap.once("error", (err) => reject(err));
    imap.connect();
  });
}
