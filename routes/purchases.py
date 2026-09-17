from flask import Blueprint, request, jsonify
from database.models import Member, Transaction
from database import db
from routes.auth import login_required

purchases_bp = Blueprint('purchases', __name__)

@purchases_bp.route('/', methods=['POST'])
@login_required
def add_purchase():
    data = request.json
    member = Member.query.filter_by(phone=data.get('phone')).first()
    if not member:
        return jsonify({"error": "Member not found"}), 404

    amount = float(data.get('amount', 0))
    
    # 1. Apply Tier Multipliers
    multiplier = 1.0
    if member.tier == 'SILVER': multiplier = 1.5
    if member.tier == 'GOLD': multiplier = 2.0
    
    points_to_add = int(amount * multiplier)
    
    # 2. Add to Ledger
    tx = Transaction(
        member_id=member.id, 
        tx_type='EARN', 
        points=points_to_add, 
        description=f"${amount} Purchase"
    )
    db.session.add(tx)
    db.session.commit() # Save first so lifetime points update
    
    # 3. Check if they earned a Tier upgrade
    member.evaluate_tier()
    db.session.commit()

    return jsonify({
        "message": f"Added {points_to_add} points", 
        "member": member.to_dict()
    }), 200