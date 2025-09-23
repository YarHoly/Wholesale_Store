from app import create_app
from app.models import User, db

app = create_app()

with app.app_context():
    user_count = User.query.count()

    if user_count == 0:
        print("Нет пользователей для удаления")
        exit()
    
    confirm = input("Это удалит ВСЕХ пользователей. Продолжить? (y/n): ")
    
    if confirm.lower() == 'y':
        try:        
            deleted_count = User.query.delete()
            db.session.commit()
            print(f"Успешно удалено {deleted_count} пользователей")
        except Exception as e:
            db.session.rollback()
            print(f" Ошибка при удалении: {e}")
    else:
        print(" Удаление отменено")