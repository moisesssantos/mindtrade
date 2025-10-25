// api/test-db.js
import { Client } from "pg";

export default async function handler(req, res) {
  const client = new Client({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false },
  });

  try {
    await client.connect();
    const result = await client.query("SELECT NOW() as current_time");
    res.status(200).json({
      success: true,
      message: "Conexão com o Neon bem-sucedida!",
      data: result.rows[0],
    });
  } catch (error) {
    console.error("Erro ao conectar:", error);
    res.status(500).json({ success: false, error: error.message });
  } finally {
    await client.end();
  }
}
