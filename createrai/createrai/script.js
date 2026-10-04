// ==========================================
// CREATORAI CONFIGURATION
// ==========================================

const API_URL = "http://127.0.0.1:5000";


// ==========================================
// NEW PROJECT MODAL
// ==========================================

const newProjectButton =
    document.querySelector("#newProjectBtn");

const projectModal =
    document.querySelector("#projectModal");

const closeModal =
    document.querySelector("#closeModal");

const createProjectButton =
    document.querySelector("#createProjectBtn");


if (newProjectButton && projectModal) {

    newProjectButton.addEventListener(
        "click",
        function () {

            projectModal.classList.add("show");

        }
    );

}


if (closeModal && projectModal) {

    closeModal.addEventListener(
        "click",
        function () {

            projectModal.classList.remove("show");

        }
    );

}


// ==========================================
// CREATE PROJECT
// ==========================================

if (createProjectButton) {

    createProjectButton.addEventListener(
        "click",
        async function () {

            const projectNameInput =
                document.querySelector("#projectName");

            const contentTypeInput =
                document.querySelector("#contentType");

            if (!projectNameInput) {
                return;
            }

            const projectName =
                projectNameInput.value.trim();

            const contentType =
                contentTypeInput
                    ? contentTypeInput.value
                    : "Short Video";

            if (!projectName) {

                alert(
                    "Please enter a project name."
                );

                return;

            }

            createProjectButton.disabled =
                true;

            createProjectButton.textContent =
                "Creating...";

            try {

                const response = await fetch(
                    `${API_URL}/api/projects`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            project_name:
                                projectName,

                            content_type:
                                contentType

                        })
                    }
                );

                const data =
                    await response.json();

                if (data.status === "success") {

                    alert(
                        "Project created successfully!"
                    );

                    if (projectModal) {

                        projectModal.classList.remove(
                            "show"
                        );

                    }

                } else {

                    alert(
                        data.message ||
                        "Could not create project."
                    );

                }

            } catch (error) {

                console.error(error);

                alert(
                    "Could not connect to CreatorAI backend."
                );

            }

            createProjectButton.disabled =
                false;

            createProjectButton.textContent =
                "Create Project";

        }
    );

}


// ==========================================
// SCRIPT FILE
// ==========================================

const scriptFile =
    document.querySelector("#scriptFile");

const scriptUploadStatus =
    document.querySelector(
        "#scriptUploadStatus"
    );


if (scriptFile) {

    scriptFile.addEventListener(
        "change",
        function () {

            if (!scriptFile.files.length) {
                return;
            }

            const file =
                scriptFile.files[0];

            if (scriptUploadStatus) {

                scriptUploadStatus.textContent =
                    `Selected: ${file.name}`;

            }

        }
    );

}


// ==========================================
// VIDEO FILE
// ==========================================

const videoFile =
    document.querySelector("#videoFile");

const videoUploadStatus =
    document.querySelector(
        "#videoUploadStatus"
    );


if (videoFile) {

    videoFile.addEventListener(
        "change",
        function () {

            if (!videoFile.files.length) {
                return;
            }

            const file =
                videoFile.files[0];

            if (videoUploadStatus) {

                videoUploadStatus.textContent =
                    `Selected: ${file.name}`;

            }

        }
    );

}


// ==========================================
// ANALYZE FOOTAGE
// ==========================================

const analyzeButton =
    document.querySelector(
        "#analyzeButton"
    );


if (analyzeButton) {

    analyzeButton.addEventListener(
        "click",
        async function () {

            const scriptInput =
                document.querySelector(
                    "#scriptFile"
                );

            const videoInput =
                document.querySelector(
                    "#videoFile"
                );

            const scriptText =
                document.querySelector(
                    "#scriptText"
                );


            // ----------------------------------
            // SCRIPT VALIDATION
            // ----------------------------------

            const hasScriptFile =
                scriptInput &&
                scriptInput.files.length > 0;

            const hasScriptText =
                scriptText &&
                scriptText.value.trim() !== "";


            if (!hasScriptFile && !hasScriptText) {

                alert(
                    "Please upload a script or paste your script."
                );

                return;

            }


            // ----------------------------------
            // VIDEO VALIDATION
            // ----------------------------------

            if (
                !videoInput ||
                !videoInput.files.length
            ) {

                alert(
                    "Please select a video file."
                );

                return;

            }


            // ----------------------------------
            // BUTTON
            // ----------------------------------

            analyzeButton.disabled = true;

            analyzeButton.textContent =
                "Analyzing...";


            // ----------------------------------
            // FORM DATA
            // ----------------------------------

            const formData =
                new FormData();


            if (hasScriptFile) {

                formData.append(
                    "script",
                    scriptInput.files[0]
                );

            }


            if (hasScriptText) {

                formData.append(
                    "script_text",
                    scriptText.value
                );

            }


            formData.append(
                "video",
                videoInput.files[0]
            );


            try {

                const response =
                    await fetch(
                        `${API_URL}/api/analyze`,
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                const data =
                    await response.json();


                console.log(
                    "CreatorAI Analysis:",
                    data
                );


                if (!response.ok) {

                    alert(
                        data.message ||
                        "Analysis failed."
                    );

                    return;

                }


                displayMatches(
                    data.matches || []
                );


                displayClips(
                    data.smart_clips || []
                );


                alert(
                    "CreatorAI analysis completed!"
                );


            } catch (error) {

                console.error(
                    "Analysis error:",
                    error
                );

                alert(
                    "Could not connect to CreatorAI backend."
                );

            }


            analyzeButton.disabled =
                false;

            analyzeButton.textContent =
                "Analyze Footage →";

        }
    );

}


// ==========================================
// DISPLAY MATCHES
// ==========================================

function displayMatches(matches) {

    const matchResults =
        document.querySelector(
            "#matchResults"
        );


    if (!matchResults) {
        return;
    }


    if (!matches.length) {

        matchResults.innerHTML = `

            <div class="match-card">

                <div class="match-content">

                    <span class="match-label">
                        NO MATCHES
                    </span>

                    <h3>
                        No matching footage found.
                    </h3>

                </div>

            </div>

        `;

        return;

    }


    matchResults.innerHTML = "";


    matches.forEach(
        function (match) {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "match-card";


            card.innerHTML = `

                <div class="match-content">

                    <span class="match-label">
                        SCRIPT SECTION
                    </span>

                    <h3>
                        "${escapeHTML(
                            match.title
                        )}"
                    </h3>

                </div>

                <div class="match-result">

                    <div class="timestamp">

                        ${match.start_time}
                        —
                        ${match.end_time}

                    </div>

                    <div class="match-score">

                        ${match.match_score}%
                        Match

                    </div>

                </div>

            `;


            matchResults.appendChild(
                card
            );

        }
    );

}


// ==========================================
// DISPLAY SMART CLIPS
// ==========================================

function displayClips(clips) {

    const clipsGrid =
        document.querySelector(
            "#clipsGrid"
        );


    if (!clipsGrid) {
        return;
    }


    clipsGrid.innerHTML = "";


    if (!clips.length) {

        clipsGrid.innerHTML = `

            <div class="clip-card">

                <div class="clip-preview">
                    —
                </div>

                <div class="clip-info">

                    <h3>
                        No clips found
                    </h3>

                    <p>
                        Try another video.
                    </p>

                </div>

            </div>

        `;

        return;

    }


    clips.forEach(
        function (clip, index) {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "clip-card";


            card.innerHTML = `

                <div class="clip-preview">
                    ▶
                </div>

                <div class="clip-info">

                    <h3>
                        ${escapeHTML(
                            clip.title ||
                            `Clip ${index + 1}`
                        )}
                    </h3>

                    <p>

                        ${clip.start_time}
                        —
                        ${clip.end_time}

                    </p>

                    <p>

                        ${clip.score}%
                        Match

                    </p>

                    <small>

                        ${escapeHTML(
                            clip.platform ||
                            "CreatorAI"
                        )}

                    </small>

                </div>

            `;


            clipsGrid.appendChild(
                card
            );

        }
    );

}


// ==========================================
// HTML SAFETY
// ==========================================

function escapeHTML(value) {

    if (value === undefined || value === null) {
        return "";
    }

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


// ==========================================
// SAVE PROJECT
// ==========================================

const saveProjectButton =
    document.querySelector(
        "#saveProjectButton"
    );


if (saveProjectButton) {

    saveProjectButton.addEventListener(
        "click",
        function () {

            alert(
                "Project saved successfully!"
            );

        }
    );

}


// ==========================================
// BACKEND STATUS
// ==========================================

async function checkBackend() {

    try {

        const response =
            await fetch(
                `${API_URL}/api/status`
            );


        const data =
            await response.json();


        console.log(
            "CreatorAI Backend:",
            data
        );


    } catch (error) {

        console.warn(
            "CreatorAI backend is offline."
        );

    }

}


checkBackend();