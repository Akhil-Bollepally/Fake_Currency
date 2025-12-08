import cv2, os

def check_currency(image_path):
    img = cv2.imread(image_path, 0)
    img = cv2.resize(img, (400, 200))

    real_folder = "models/real"
    fake_folder = "models/fake"

    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    best_real = 0
    best_fake = 0

    # Check Real Notes
    for real_img in os.listdir(real_folder):
        sample = cv2.imread(os.path.join(real_folder, real_img), 0)
        sample = cv2.resize(sample, (400, 200))
        kp2, des2 = orb.detectAndCompute(sample, None)
        if des1 is not None and des2 is not None:
            matches = bf.match(des1, des2)
            best_real = max(best_real, len(matches))

    # Check Fake Notes
    for fake_img in os.listdir(fake_folder):
        sample = cv2.imread(os.path.join(fake_folder, fake_img), 0)
        sample = cv2.resize(sample, (400, 200))
        kp2, des2 = orb.detectAndCompute(sample, None)
        if des1 is not None and des2 is not None:
            matches = bf.match(des1, des2)
            best_fake = max(best_fake, len(matches))

    print("Best Real Matches:", best_real)
    print("Best Fake Matches:", best_fake)

    # Decide result
    if best_real == 0 and best_fake == 0:
        return "UNKNOWN"
    elif best_real > best_fake:
        return "REAL"
    elif best_fake > best_real:
        return "FAKE"
    else:
        return "UNKNOWN"
