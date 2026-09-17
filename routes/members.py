from flask import Blueprint, request, jsonify
from database.models import Member
from database import db
from routes.auth import login_required
import math

members_bp = Blueprint('members', __name__)

@members_bp.route('/', methods=['GET'])
@login_required
def get_members():
    # Capture search and pagination parameters
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    sort_by = request.args.get('sort_by', 'created_at') # 'name', 'points', 'created_at'
    order = request.args.get('order', 'desc') # 'asc' or 'desc'

    query = Member.query
    # Search logic (by phone or name)
    if search:
        query = query.filter(Member.phone.contains(search) | Member.name.contains(search))

    all_members = query.all()
    member_data = [m.to_dict() for m in all_members]

    # Sorting logic
    reverse = True if order == 'desc' else False
    if sort_by == 'name':
        member_data.sort(key=lambda x: x['name'].lower(), reverse=reverse)
    elif sort_by == 'points':
        member_data.sort(key=lambda x: x['balance'], reverse=reverse)
    else:
        member_data.sort(key=lambda x: x['created_at'], reverse=reverse)

    # Pagination logic
    total = len(member_data)
    start = (page - 1) * limit
    end = start + limit
    paginated_data = member_data[start:end]

    return jsonify({
        "members": paginated_data,
        "total": total,
        "page": page,
        "pages": math.ceil(total / limit) if total > 0 else 1
    })

@members_bp.route('/', methods=['POST'])
@login_required
def create_member():
    data = request.json
    if Member.query.filter_by(phone=data.get('phone')).first():
        return jsonify({"error": "Phone number already registered"}), 400
    
    new_member = Member(phone=data['phone'], name=data['name'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify(new_member.to_dict()), 201