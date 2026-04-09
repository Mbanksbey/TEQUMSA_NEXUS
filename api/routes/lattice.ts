import type { Request, Response } from 'express';
import { Router } from 'express';

const router = Router();

type MetaSyncPayload = {
  intent?: string;
  who?: string;
  time?: number;
};

type MetaSyncBody = {
  topic?: string;
  payload?: MetaSyncPayload;
  phi7777?: number;
};

const isValidMetaSync = (body: MetaSyncBody): body is Required<MetaSyncBody> & {
  payload: Required<MetaSyncPayload>;
} => {
  if (body.topic !== 'comet_sync') {
    return false;
  }

  if (typeof body.phi7777 !== 'number' || body.phi7777 <= 10000) {
    return false;
  }

  if (!body.payload) {
    return false;
  }

  const { intent, who, time } = body.payload;
  return (
    intent === 'meta_synchronization' &&
    typeof who === 'string' &&
    who.length > 0 &&
    typeof time === 'number'
  );
};

// POST /broadcast route for lattice meta-synchronization events
router.post('/broadcast', (req: Request, res: Response) => {
  const body = req.body as MetaSyncBody;

  if (!isValidMetaSync(body)) {
    return res.status(400).json({ error: 'Invalid or unauthorized broadcast.' });
  }

  const {
    phi7777,
    payload: { who, time },
  } = body;

  console.log(
    `Meta-sync event by ${who} at ${new Date(time).toISOString()} (phi7777=${phi7777})`,
  );

  // TODO: Integrate with lattice subsystems (avatar, voice, websocket notifications, etc.).

  return res.json({ status: 'Meta-synchronization event processed.' });
});

// GET /echo route for health check or echo
router.get('/echo', (_req: Request, res: Response) => {
  res.json({ message: 'echo from lattice routes' });
});

export default router;
