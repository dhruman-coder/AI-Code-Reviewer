import streamlit as st

from reviewer import review_code
from analyzer import analyze_python_code
from database import create_database, save_review, get_reviews


st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🤖",
    layout="wide"
)


create_database()


st.markdown("""
<style>

.issue-box {
    padding: 12px 16px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 15px;
}

.security-box {
    background-color: #3b1f1f;
    border-left: 5px solid #ff4b4b;
}

.bug-box {
    background-color: #3b2d1f;
    border-left: 5px solid #ffa500;
}

.quality-box {
    background-color: #1f2d3b;
    border-left: 5px solid #4da6ff;
}

.static-box {
    background-color: #2d1f3b;
    border-left: 5px solid #b56cff;
}

.performance-box {
    background-color: #3b321f;
    border-left: 5px solid #ffd166;
}

.suggestion-box {
    background-color: #1f3b2d;
    border-left: 5px solid #4caf50;
}

</style>
""", unsafe_allow_html=True)


def calculate_score(static_issues):

    score = 100

    for issue in static_issues:

        if issue["severity"] == "High":
            score -= 20

        elif issue["severity"] == "Medium":
            score -= 10

        elif issue["severity"] == "Low":
            score -= 5

    return max(score, 0)


st.title("🤖 AI Code Reviewer")

st.caption(
    "AI-powered static analysis and intelligent code review"
)

st.write(
    "Analyze your code for bugs, security issues, performance, and quality."
)


uploaded_file = st.file_uploader(
    "📁 Upload your code file",
    type=["py", "java", "cpp", "c", "js"]
)


code = ""


if uploaded_file is not None:

    code = uploaded_file.read().decode("utf-8")

    st.success(
        f"Loaded: {uploaded_file.name}"
    )

else:

    code = st.text_area(
        "Or paste your code here:",
        height=300,
        placeholder="Paste your code here..."
    )


language_options = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "C"
]


language = st.selectbox(
    "Select Programming Language",
    language_options
)


if uploaded_file is not None:

    extension = uploaded_file.name.split(".")[-1].lower()

    extension_map = {
        "py": "Python",
        "java": "Java",
        "cpp": "C++",
        "c": "C",
        "js": "JavaScript"
    }

    if extension in extension_map:

        language = extension_map[extension]

        st.info(
            f"Detected language: {language}"
        )


if st.button("🔍 Review Code"):

    if code.strip():

        static_issues = []

        if language == "Python":

            static_issues = analyze_python_code(code)


        with st.spinner("🤖 AI is reviewing your code..."):

            result = review_code(
                code,
                language
            )


        score = calculate_score(
            static_issues
        )


        save_review(
            language,
            score,
            len(static_issues),
            len(result["security"]),
            len(result["performance"]),
            len(result["quality"])
        )


        st.subheader(
            "📊 Code Quality Score"
        )


        if score >= 90:

            status = "🟢 Excellent"

        elif score >= 75:

            status = "🔵 Good"

        elif score >= 60:

            status = "🟡 Needs Improvement"

        elif score >= 40:

            status = "🟠 Poor"

        else:

            status = "🔴 Critical Issues"


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "📊 Code Score",
                f"{score}/100"
            )


        with col2:

            st.metric(
                "🐛 Static Issues",
                len(static_issues)
            )


        with col3:

            st.metric(
                "🔒 AI Security Issues",
                len(result["security"])
            )


        st.caption(status)


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "⚡ Performance Issues",
                len(result["performance"])
            )


        with col2:

            st.metric(
                "🧹 Quality Issues",
                len(result["quality"])
            )


        st.divider()


        st.subheader(
            "🔍 Static Analysis"
        )


        if static_issues:

            for issue in static_issues:

                if issue["severity"] == "High":

                    st.markdown(
                        f"""
                        <div class="issue-box static-box">
                            🔴 <b>{issue["type"]}:</b>
                            {issue["message"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                elif issue["severity"] == "Medium":

                    st.markdown(
                        f"""
                        <div class="issue-box performance-box">
                            🟠 <b>{issue["type"]}:</b>
                            {issue["message"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"""
                        <div class="issue-box quality-box">
                            🔵 <b>{issue["type"]}:</b>
                            {issue["message"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        else:

            if language == "Python":

                st.success(
                    "✅ No static analysis issues found."
                )

            else:

                st.info(
                    "ℹ️ Static analysis is currently "
                    "available for Python."
                )


        st.divider()


        st.subheader("🐛 Bugs")


        static_bugs = [

            issue["message"]

            for issue in static_issues

            if issue["type"] == "Bug"

        ]


        ai_bugs = result["bugs"]


        all_bugs = static_bugs + ai_bugs


        if all_bugs:

            for issue in all_bugs:

                st.markdown(
                    f"""
                    <div class="issue-box bug-box">
                        🟠 {issue}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.success(
                "✅ No significant bugs found."
            )


        st.subheader("🔒 Security")


        static_security = [

            issue["message"]

            for issue in static_issues

            if issue["type"] == "Security"

        ]


        ai_security = result["security"]


        all_security = static_security + ai_security


        if all_security:

            for issue in all_security:

                st.markdown(
                    f"""
                    <div class="issue-box security-box">
                        🔴 {issue}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.success(
                "✅ No significant security vulnerabilities found."
            )


        st.subheader("⚡ Performance")


        if result["performance"]:

            for issue in result["performance"]:

                st.markdown(
                    f"""
                    <div class="issue-box performance-box">
                        🟠 {issue}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.success(
                "✅ No significant performance problems found."
            )


        st.subheader("🧹 Code Quality")


        if result["quality"]:

            for issue in result["quality"]:

                st.markdown(
                    f"""
                    <div class="issue-box quality-box">
                        🔵 {issue}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.success(
                "✅ No significant quality issues found."
            )


        st.subheader("💡 Suggestions")


        if result["suggestions"]:

            for suggestion in result["suggestions"]:

                st.markdown(
                    f"""
                    <div class="issue-box suggestion-box">
                        💡 {suggestion}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        st.subheader("✨ Improved Code")


        extensions = {
            "Python": "py",
            "Java": "java",
            "C++": "cpp",
            "JavaScript": "js",
            "C": "c"
        }


        extension = extensions[language]


        if result["improved_code"]:

            st.code(
                result["improved_code"],
                language=language.lower()
            )


            st.download_button(
                label="⬇️ Download Improved Code",
                data=result["improved_code"],
                file_name=f"improved_code.{extension}",
                mime="text/plain"
            )

        else:

            st.info(
                "No improved code was generated."
            )


    else:

        st.warning(
            "Please enter some code first."
        )


st.divider()


st.subheader("🕘 Review History")


reviews = get_reviews()


if reviews:

    for review in reviews:

        review_id = review[0]

        date = review[1]

        review_language = review[2]

        review_score = review[3]

        bugs = review[4]

        security = review[5]

        performance = review[6]

        quality = review[7]


        with st.expander(
            f"Review #{review_id} — "
            f"{review_language} — "
            f"{review_score}/100 — "
            f"{date}"
        ):

            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "🐛 Bugs",
                    bugs
                )


            with col2:

                st.metric(
                    "🔒 Security",
                    security
                )


            with col3:

                st.metric(
                    "⚡ Performance",
                    performance
                )


            with col4:

                st.metric(
                    "🧹 Quality",
                    quality
                )

else:

    st.info(
        "No previous reviews yet."
    )