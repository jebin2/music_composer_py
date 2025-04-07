// Music Generation App - Organized JavaScript

/**
 * Constants and DOM References
 */
// Theme and UI elements
const html = document.documentElement;
const themeToggle = document.getElementById('themeToggle');
const settingsToggle = document.getElementById('settingsToggle');
const settingsModal = document.getElementById('settingsModal');
const closeSettings = document.getElementById('closeSettings');
const saveSettings = document.getElementById('save_settings');

// Music and instrument controls
const instrumentList = document.getElementById('instrumentList');
let instrumentButtons = instrumentList.querySelectorAll('.instrument-button');
const selectAllButton = document.querySelector('.select-all-button');
const generateButton = document.querySelector('.generate-button');
const downloadButton = document.querySelector('.download-button');

// Audio player elements
const playButton = document.querySelector('.play-button');
const audio = document.getElementById('audioPlayer');
const timeDisplay = document.querySelector('.time-display');
const waveformElement = document.querySelector('.waveform');
const textInput = document.getElementById("textInput");

/**
 * SVG Icons
 */
const ICONS = {
	sun: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`,
	moon: `
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" 
     viewBox="0 0 24 24" fill="none" stroke="currentColor" 
     stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 12.79A9 9 0 1 1 11.21 3a7 7 0 0 0 9.79 9.79z"/>
</svg>`,
	play: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`,
	pause: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>`
};

/**
 * State Variables
 */
let state = {
	isPlaying: false,
	selectedInstruments: new Set(),
	allInstrumentsSelected: true
};

/**
 * Utility Functions
 */
// Format time in MM:SS format
function formatTime(seconds) {
	if (isNaN(seconds) || seconds === Infinity) return "00:00";
	const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
	const secs = Math.floor(seconds % 60).toString().padStart(2, '0');
	return `${mins}:${secs}`;
}

// Load audio file
function loadAudio() {
	audio.src = "/static/output.wav";
	audio.load();
}

/**
 * Theme Management
 */
const ThemeManager = {
	apply: function (theme) {
		html.setAttribute('data-theme', theme);
		themeToggle.innerHTML = theme === 'dark' ? ICONS.sun : ICONS.moon;
		themeToggle.title = theme === 'dark' ? "Switch to Light Theme" : "Switch to Dark Theme";
	},

	toggle: function () {
		const current = html.getAttribute('data-theme');
		this.apply(current === 'dark' ? 'light' : 'dark');
	},

	initialize: function () {
		themeToggle.addEventListener('click', () => this.toggle());
		this.apply('dark'); // Default theme
	}
};

/**
 * Settings Modal Manager
 */
const SettingsManager = {
	open: function () {
		settingsModal.style.display = 'flex';
	},

	close: function () {
		settingsModal.style.display = 'none';
	},

	save: async function () {
		await fetch('/api/settings', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				api_key: document.getElementById("apiKey").value
			})
		});
		this.close();
	},

	initialize: async function () {
		settingsToggle.addEventListener('click', () => this.open());
		closeSettings.addEventListener('click', () => this.close());
		settingsModal.addEventListener('click', e => {
			if (e.target === settingsModal) this.close();
		});
		saveSettings.addEventListener('click', () => this.save());

		// Fetch and populate existing settings on init
		try {
			const res = await fetch('/api/settings');
			const data = await res.json();
			if (data.api_key) {
				document.getElementById("apiKey").value = data.api_key.replace(/^"|"$/g, ''); // Remove extra quotes if present
				instruments = data.instruments;
				InstrumentManager.initialize();
			}
		} catch (err) {
			console.error("Failed to load settings:", err);
		}
	}
};


/**
 * Instrument Selection Manager
 */
let instruments = ['piano', 'guitar', 'violin'];

const InstrumentManager = {
	updateButtonStyles: function () {
		let allSelected = true;
		instrumentButtons = instrumentList.querySelectorAll('.instrument-button'); // Re-select in case new buttons added

		instrumentButtons.forEach(button => {
			const instrument = button.dataset.instrument;
			if (state.selectedInstruments.has(instrument)) {
				button.classList.add('selected');
			} else {
				button.classList.remove('selected');
				allSelected = false;
			}
		});

		state.allInstrumentsSelected = allSelected;
		selectAllButton.classList.toggle('selected', allSelected);
		selectAllButton.title = allSelected ? "Deselect All" : "Select All";
	},

	toggleInstrument: function (instrument) {
		if (state.selectedInstruments.has(instrument)) {
			state.selectedInstruments.delete(instrument);
		} else {
			state.selectedInstruments.add(instrument);
		}
		this.updateButtonStyles();
	},

	toggleAll: function () {
		const selectAll = !selectAllButton.classList.contains('selected');
		instrumentButtons = instrumentList.querySelectorAll('.instrument-button'); // Ensure buttons are up to date

		if (selectAll) {
			instrumentButtons.forEach(btn => state.selectedInstruments.add(btn.dataset.instrument));
		} else {
			state.selectedInstruments.clear();
		}
		this.updateButtonStyles();
	},

	renderButtons: function () {
		instrumentList.innerHTML = ''; // Clear existing
		instruments.forEach(name => {
			const button = document.createElement('button');
			button.className = 'instrument-button';
			button.dataset.instrument = name;
			button.textContent = name.charAt(0).toUpperCase() + name.slice(1); // Capitalize
			instrumentList.appendChild(button);
		});
	},

	initialize: function () {
		this.renderButtons();

		// Select all instruments by default
		instruments.forEach(instrument => state.selectedInstruments.add(instrument));

		// Attach click handlers
		instrumentList.addEventListener('click', (e) => {
			if (!e.target.classList.contains('instrument-button')) return;
			this.toggleInstrument(e.target.dataset.instrument);
		});

		selectAllButton.addEventListener('click', () => this.toggleAll());

		this.updateButtonStyles();
	}
};


/**
 * Music Generation Manager
 */
const MusicGenerator = {
	async generate() {
		let currentSelection = Array.from(state.selectedInstruments);

		// Check if we should use all instruments or selected ones
		if (state.allInstrumentsSelected) {
			currentSelection = null;
		} else if (currentSelection.length === 0) {
			alert("Please select at least one instrument before generating!");
			return;
		}

		// Update UI state
		generateButton.disabled = true;
		generateButton.textContent = "Imagine...";

		try {
			const response = await fetch('/api/generate', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					text: textInput.value,
					instruments: currentSelection
				})
			});

			const data = await response.json();
			if (!response.ok) {
				throw new Error(data.message || 'Generation failed');
			}

			loadAudio();
		} catch (err) {
			console.error("Error generating music:", err);
			alert("There was an error generating music. Please try again.");
		} finally {
			generateButton.disabled = false;
			generateButton.textContent = "Generate Music";
		}
	},

	initialize: function () {
		generateButton.addEventListener('click', () => this.generate());
	}
};

/**
 * Audio Player Manager
 */
const AudioPlayer = {
	togglePlayback: function () {
		if (state.isPlaying) {
			audio.pause();
			waveformElement.classList.remove('is-playing');
			// state.isPlaying will be updated in the 'pause' event listener
		} else {
			audio.play()
				.then(() => {
					waveformElement.classList.add('is-playing');
					// state.isPlaying will be updated in the 'play' event listener
				})
				.catch(err => {
					console.error("Error playing audio:", err);
				});
			// Don't touch state.isPlaying here — let 'play' event handle it
		}
	},


	updatePlayIcon: function (isPlaying) {
		playButton.innerHTML = isPlaying ? ICONS.pause : ICONS.play;
	},

	updateTimeDisplay: function () {
		timeDisplay.textContent = `${formatTime(audio.currentTime)} / ${formatTime(audio.duration)}`;
	},

	initialize: function () {
		// Set up event listeners
		playButton.addEventListener('click', () => this.togglePlayback());

		audio.addEventListener('play', () => {
			state.isPlaying = true;
			this.updatePlayIcon(true);
		});

		audio.addEventListener('pause', () => {
			state.isPlaying = false;
			this.updatePlayIcon(false);
		});

		audio.addEventListener('loadedmetadata', () => {
			this.updateTimeDisplay();
		});

		audio.addEventListener('timeupdate', () => {
			this.updateTimeDisplay();
		});

		audio.addEventListener('ended', () => {
			state.isPlaying = false;
			waveformElement.classList.remove('is-playing');
			this.updatePlayIcon(false);
		});

		// Initialize UI
		this.updatePlayIcon(false);
		loadAudio();
	}
};

/**
 * Download Manager
 */
const DownloadManager = {
	download: function () {
		const link = document.createElement('a');
		link.href = "/static/output.wav";
		link.download = "generated-music.wav";
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	},

	initialize: function () {
		downloadButton.addEventListener('click', () => this.download());
	}
};

/**
 * App Initialization
 */
function initializeApp() {
	// Set default text input value
	textInput.value = `The highly classified document contained extremely sensitive information about the government's secret space exploration program, codenamed "Eclipse," which had been shrouded in mystery for decades. The existence of alien life was confirmed, sparking widespread panic and chaos throughout the world. The news was met with both awe and terror as scientists and world leaders scrambled to understand the implications. Meanwhile, a rogue agent had infiltrated the facility, intent on exploiting the discovery for personal gain. The clock was ticking, and the fate of humanity hung precariously in the balance. The world teetered on the brink of chaos as the truth about Eclipse began to unravel.`;

	// Initialize all components
	ThemeManager.initialize();
	SettingsManager.initialize();
	// InstrumentManager.initialize();
	MusicGenerator.initialize();
	AudioPlayer.initialize();
	DownloadManager.initialize();
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeApp);