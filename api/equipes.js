import { Client } from "pg";

export const config = {
  runtime: "edge",
};

export default async function handler(req) {
  const client = new Client({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false },
  });

  await client.connect();

  try {
    if (req.method === "GET") {
      const { searchParams } = new URL(req.url);
      const busca = searchParams.get("busca");
      const query = busca
        ? `SELECT * FROM equipes WHERE nome ILIKE $1 ORDER BY nome ASC`
        : `SELECT * FROM equipes ORDER BY nome ASC`;
      const values = busca ? [`%${busca}%`] : [];
      const result = await client.query(query, values);
      return new Response(JSON.stringify(result.rows), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    }

    if (req.method === "POST") {
      const body = await req.json();
      const { nome } = body;
      if (!nome) {
        return new Response(
          JSON.stringify({ error: "O campo 'nome' é obrigatório." }),
          { status: 400, headers: { "Content-Type": "application/json" } }
        );
      }

      const check = await client.query(
        "SELECT 1 FROM equipes WHERE nome ILIKE $1",
        [nome]
      );
      if (check.rowCount > 0) {
        return new Response(
          JSON.stringify({ error: "Já existe uma equipe com esse nome." }),
          { status: 409, headers: { "Content-Type": "application/json" } }
        );
      }

      await client.query("INSERT INTO equipes (nome) VALUES ($1)", [nome]);
      return new Response(
        JSON.stringify({ message: "Equipe cadastrada com sucesso!" }),
        { status: 201, headers: { "Content-Type": "application/json" } }
      );
    }

    return new Response(
      JSON.stringify({ error: `Método ${req.method} não permitido` }),
      { status: 405, headers: { "Content-Type": "application/json" } }
    );
  } catch (error) {
    console.error(error);
    return new Response(
      JSON.stringify({ error: "Erro interno no servidor." }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  } finally {
    await client.end();
  }
}
