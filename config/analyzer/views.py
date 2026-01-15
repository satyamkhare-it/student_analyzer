import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from sklearn.linear_model import LinearRegression

from .models import Student


# -------------------------
# HOME PAGE
# -------------------------
def home(request):
    return render(request, 'home.html')


# -------------------------
# FILE UPLOAD + ANALYSIS
# -------------------------
@login_required
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']

        # ==========================
        # DIRECTORIES
        # ==========================
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        plot_dir = os.path.join(settings.MEDIA_ROOT, 'plots')

        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(plot_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, file.name)

        # ==========================
        # SAVE FILE
        # ==========================
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # ==========================
        # READ CSV
        # ==========================
        df = pd.read_csv(file_path)

        """
        Expected CSV columns:
        RollNo, Name,
        Physics_Q, Physics_H, Physics_P,
        Maths_Q, Maths_H, Maths_P,
        Chemistry_Q, Chemistry_H, Chemistry_P,
        English_Q, English_H, English_P,
        Attendance
        """

        # ==========================
        # CLEAR OLD DATA
        # ==========================
        Student.objects.all().delete()

        # ==========================
        # SAVE DATA TO DB
        # ==========================
        for _, row in df.iterrows():
            Student.objects.create(
                roll_number=int(row['roll_number']),
                name=row['Name'],

                physics_q=int(row['Physics_Q']),
                physics_h=int(row['Physics_H']),
                physics_p=int(row['Physics_P']),

                maths_q=int(row['Maths_Q']),
                maths_h=int(row['Maths_H']),
                maths_p=int(row['Maths_P']),

                chemistry_q=int(row['Chemistry_Q']),
                chemistry_h=int(row['Chemistry_H']),
                chemistry_p=int(row['Chemistry_P']),

                english_q=int(row['English_Q']),
                english_h=int(row['English_H']),
                english_p=int(row['English_P']),

                attendance=int(row['Attendance'])
            )

        # ==================================================
        # ================== ANALYTICS =====================
        # ==================================================

        subjects = ['Physics', 'Maths', 'Chemistry', 'English']

        avg_marks = {
            'Physics': df[['Physics_Q', 'Physics_H', 'Physics_P']].mean().mean(),
            'Maths': df[['Maths_Q', 'Maths_H', 'Maths_P']].mean().mean(),
            'Chemistry': df[['Chemistry_Q', 'Chemistry_H', 'Chemistry_P']].mean().mean(),
            'English': df[['English_Q', 'English_H', 'English_P']].mean().mean(),
        }

        # --------------------------
        # 1. BAR CHART – Avg Marks
        # --------------------------
        plt.figure(figsize=(6, 4))
        plt.bar(avg_marks.keys(), avg_marks.values())
        plt.title('Average Marks per Subject')
        plt.ylabel('Marks')

        bar_path = os.path.join(plot_dir, 'bar_avg.png')
        plt.savefig(bar_path)
        plt.close()

        # --------------------------
        # 2. PIE CHART – Contribution
        # --------------------------
        plt.figure(figsize=(6, 6))
        plt.pie(avg_marks.values(), labels=avg_marks.keys(), autopct='%1.1f%%')
        plt.title('Subject-wise Contribution')

        pie_path = os.path.join(plot_dir, 'pie_subject.png')
        plt.savefig(pie_path)
        plt.close()

        # --------------------------
        # 3. LINE CHART – Exam Trend
        # --------------------------
        exam_avg = {
            'Quarterly': df[['Physics_Q', 'Maths_Q', 'Chemistry_Q', 'English_Q']].mean().mean(),
            'Half Yearly': df[['Physics_H', 'Maths_H', 'Chemistry_H', 'English_H']].mean().mean(),
            'Pre Final': df[['Physics_P', 'Maths_P', 'Chemistry_P', 'English_P']].mean().mean(),
        }

        plt.figure(figsize=(6, 4))
        plt.plot(exam_avg.keys(), exam_avg.values(), marker='o')
        plt.title('Exam-wise Performance Trend')
        plt.ylabel('Average Marks')

        line_path = os.path.join(plot_dir, 'line_exam.png')
        plt.savefig(line_path)
        plt.close()

        # --------------------------
        # 4. SCATTER – Attendance vs Marks
        # --------------------------
        df['Total_Marks'] = (
            df[['Physics_P', 'Maths_P', 'Chemistry_P', 'English_P']].sum(axis=1)
        )

        plt.figure(figsize=(6, 4))
        plt.scatter(df['Attendance'], df['Total_Marks'])
        plt.title('Attendance vs Final Marks')
        plt.xlabel('Attendance (%)')
        plt.ylabel('Total Marks')

        scatter_path = os.path.join(plot_dir, 'scatter_attendance.png')
        plt.savefig(scatter_path)
        plt.close()

        # ==================================================
        # ============== ML PREDICTION (TOP 3) ==============
        # ==================================================
        final_scores = df[['Name', 'Total_Marks', 'Attendance']]

        X = final_scores[['Attendance']]
        y = final_scores['Total_Marks']

        model = LinearRegression()
        model.fit(X, y)

        final_scores['Predicted_Score'] = model.predict(X)

        top_students = final_scores.sort_values(
            by='Predicted_Score', ascending=False
        ).head(3).reset_index(drop=True)

        top_students['rank'] = top_students.index + 1


        # ==========================
        # CONTEXT
        # ==========================
        context = {
            'bar_chart': settings.MEDIA_URL + 'plots/bar_avg.png',
            'pie_chart': settings.MEDIA_URL + 'plots/pie_subject.png',
            'line_chart': settings.MEDIA_URL + 'plots/line_exam.png',
            'scatter_chart': settings.MEDIA_URL + 'plots/scatter_attendance.png',
            'top_students': top_students.to_dict(orient='records')
        }

        return render(request, 'result.html', context)

    return render(request, 'upload.html')
