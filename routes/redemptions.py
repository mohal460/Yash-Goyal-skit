from flask import Blueprint, request, jsonify
from database.models import Member, Transaction
from database import db
from routes.auth import login_required

redemptions_bp = Blueprint('redemptions', __name__)

@redemptions_bp.route('/', methods=['POST'])
@login_required
def redeem_points():
    data = request.json
    member = Member.query.filter_by(phone=data.get('phone')).first()
    if not member:
        return jsonify({"error": "Member not found"}), 404

    points_to_deduct = int(data.get('points', 0))
    item_name = data.get('item', 'Reward')

    # Guard: Prevent negative balances
    if member.live_balance < points_to_deduct:
        return jsonify({"error": f"Insufficient points. Member only has {member.live_balance}."}), 400
    
    # Log deduction in Ledger
    tx = Transaction(
        member_id=member.id, 
        tx_type='REDEEM', 
        points=-points_to_deduct, 
        description=f"Redeemed: {item_name}"
    )
    db.session.add(tx)
    db.session.commit()

    return jsonify({
        "message": f"Successfully redeemed {item_name}", 
        "member": member.to_dict()
    }), 200