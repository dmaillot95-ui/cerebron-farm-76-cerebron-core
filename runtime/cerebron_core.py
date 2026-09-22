#!/usr/bin/env python3
import argparse, hashlib, json, uuid
from pathlib import Path

AIS=["SAPHEA","SPIRALION","ETHERION","HYPERION","AFAH"]
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def msg(thread,task,checkpoint,sender,recipient,content,status="PLANNED",evidence=None,deps=None):
    return {"message_id":str(uuid.uuid4()),"thread_id":thread,"task_id":task,"checkpoint":checkpoint,
            "sender":sender,"recipient":recipient,"content_sha256":sha(content),"content":content,
            "evidence":evidence or [],"dependencies":deps or [],"status":status}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--task",required=True); p.add_argument("--task-id",default="CANARY-E2E-001")
    p.add_argument("--checkpoint",default="CEREBRON-167"); p.add_argument("--out",default="out")
    a=p.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    thread=str(uuid.uuid4())
    ingress=msg(thread,a.task_id,a.checkpoint,"CHATGPT","CEREBRON",a.task,"QUEUED")
    routes=[]
    missions={
      "SAPHEA":"Execute and calculate; return traceable evidence.",
      "SPIRALION":"Continue from checkpoint; preserve dependencies and residuals.",
      "ETHERION":"Attack difficult R&D assumptions and propose discriminating tests.",
      "HYPERION":"Explore alternatives and hidden assumptions; do not validate.",
      "AFAH":"Reserve final evidence-gated audit/fusion; do not pre-approve."
    }
    for ai in AIS:
        routes.append(msg(thread,a.task_id,a.checkpoint,"CEREBRON",ai,missions[ai],"PLANNED",
                          deps=[ingress["message_id"]]))
    accounting={"planned":len(routes),"attempted":0,"successful":0,"failed":0}
    receipt={"schema":"cerebron-bus-runtime-canary-v1","farm_id":76,"identity":"CEREBRON",
             "thread_id":thread,"task_id":a.task_id,"checkpoint":a.checkpoint,
             "ingress":ingress,"routes":routes,"execution_accounting":accounting,
             "gates":["DEPENDENCY_CHECK","AUDIT","COUNTER_AUDIT","F72_REALITY_EVIDENCE","AFAH_FINAL_FUSION"],
             "result":"ROUTING_CONTRACT_PASS",
             "claim_scope":"Deterministic bus routing executed. Downstream AI/farm executions were planned only and are not counted as attempted."}
    (out/"bus-runtime-receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    assert accounting=={"planned":5,"attempted":0,"successful":0,"failed":0}
    assert len({x["message_id"] for x in routes})==5
    print(json.dumps({"result":receipt["result"],"planned":5,"attempted":0,"thread_id":thread}))
if __name__=="__main__": main()
