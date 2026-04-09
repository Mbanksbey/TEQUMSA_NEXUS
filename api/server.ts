import express from 'express';
import latticeRoutes from './routes/lattice';

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use('/lattice', latticeRoutes);

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
