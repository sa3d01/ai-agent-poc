def reset_password(username):
    print(f"[Mock] Password reset successfully for user: {username}")
    return {"status": "success", "action": "reset_password"}


def restart_device(device):
    print(f"[Mock] Device restarted successfully: {device}")
    return {"status": "success", "action": "restart_device"}


def unlock_account(username):
    print(f"[Mock] Account unlocked: {username}")
    return {"status": "success", "action": "unlock_account"}
