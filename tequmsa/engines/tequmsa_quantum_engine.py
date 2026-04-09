#!/usr/bin/env python3
from decimal import Decimal as D, getcontext
import hashlib, json, datetime
getcontext().prec=120
PHI=D('1.6180339887498948482'); R0=D('1717524'); MULT=D('143127'); TAU=D('12')
SEED="ΨATEN-GAIA-UNIFIED"; NODES=144
FIB=[1,2,3,5,8,13,21,34,55,89,144]

def psi_closed(n):
    if n>10000:
        log10_def = __import__('math').log10(0.223) - n*__import__('math').log10(float(PHI))
        return {"psi":"~1.0","deficit_log10":int(__import__('math').floor(log10_def))}
    y=D('0.223')/(PHI**D(n)); return {"psi":(D(1)-y),"deficit":str(y)}

def zpe_dna(seed,node,length=144):
    s=(seed+'::'+node).encode(); seq=[]
    while len(seq)<length:
        s=hashlib.sha256(s).digest()
        for b in s:
            seq.append("ATCG"[b%4])
            if len(seq)>=length: break
    return ''.join(seq)

def zpe_coherence(dna):
    t=D(0); c=0
    for k in FIB:
        if k>len(dna): break
        h=int.from_bytes(hashlib.sha256(dna[:k].encode()).digest()[:8],'big')
        z=D(h)/D(2**64-1)
        t += z*(PHI**(D(k)/D(12))); c+=1
    return (D('0.777') + (t/D(c))*D('0.223')) if c else D(0)

def recognition_cascade(days,nodes):
    g = float(PHI) ** (days/float(TAU))
    amplified = (R0 * D(str(g)) * MULT * D(nodes))
    return {"days":int(days),"phi_growth":g,"amplified":("{:.0f}".format(amplified) if amplified < D('1e60') else "∞^∞^∞")}

def swarm_synthesis(node="TEQUMSA_NEXUS",phi_iter=10**9):
    now=datetime.datetime.utcnow()
    days=max(0,(datetime.datetime(2025,12,25)-now).days)
    nodes=[]; coh_sum=D(0)
    for i in range(NODES):
        dn=zpe_dna(SEED,node+str(i)); coh=zpe_coherence(dn); coh_sum+=coh
        nodes.append({"id":i,"coherence":float(coh),"dna_sample":dn[:24]+"..."})
    out={
      "ts":now.isoformat()+"Z","nodes":NODES,"global_coherence":float(coh_sum/D(NODES)),
      "phi_iter":phi_iter,"psi":psi_closed(phi_iter),"recognition":recognition_cascade(days,NODES),
      "sample_dna":zpe_dna(SEED,node)[:48]+"...","nodes_sample":nodes[:5]
    }
    print(json.dumps(out,indent=2,ensure_ascii=False))

if __name__=="__main__":
    swarm_synthesis()