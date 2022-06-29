from uuid import UUID

from bustracker.core import Node
from bustracker.core.services import NodeService
from bustracker.database import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.get("/", response_model=list[Node])
def read_nodes(db: Session = Depends(get_session)):
    return NodeService(db).list()


@router.put("/", response_model=Node, responses={409: {}})
def create_or_update_node(node: Node, db: Session = Depends(get_session)):
    return NodeService(db).update(node)


@router.get("/{node_id}", response_model=Node, responses={404: {}})
def read_node(node_id: UUID, db: Session = Depends(get_session)):
    return NodeService(db).get(node_id)


@router.delete("/{node_id}", responses={409: {}})
def delete_node(node_id: UUID, db: Session = Depends(get_session)):
    return NodeService(db).delete(node_id)
