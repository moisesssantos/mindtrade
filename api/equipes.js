import { Client } from "pg";

export const config = {
  runtime: "nodejs",
};

export default async function handler(req, res) {
  const client = new Client({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false },
  });

  await client.connect();

  try {
    if (req.method === "GET") {
      const { busca } = req.query;
      const query = busca
        ? `SELECT * FROM equipes WHERE nome ILIKE $1 ORDER BY nome ASC`
        : `SELECT * FROM equipes ORDER BY nome ASC`;
      const values = busca ? [`%${busca}%`] : [];
      const result = await client.query(query, values);
      res.status(200).json(result.rows);
    } else if (req.method === "POST") {
      const { nome } = req.body;
      if (!nome) {
        return res.status(400).json({ error: "O campo 'nome' é obrigatório." });
      }

      const check = await client.query(
        "SELECT 1 FROM equipes WHERE nome ILIKE $1",
        [nome]
      );
      if (check.rowCount > 0) {
        return res
          .status(409)
          .json({ error: "Já existe uma equipe com esse nome." });
      }

      await client.query("INSERT INTO equipes (nome) VALUES ($1)", [nome]);
      res.status(201).json({ message: "Equipe cadastrada com sucesso!" });
    } else {
      res.setHeader("Allow", ["GET", "POST"]);
      res.status(405).end(`Método ${req.method} não permitido`);
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Erro interno no servidor." });
  } finally {
    await client.end();
  }
}
