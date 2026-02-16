# C4U.studio

Minimalist 3D home decor — landing page and 3D customization demo.

How the 3D customization works
- A single `<model-viewer id="mainViewer">` is used on the page.
- Default model is a text-based tile (`models/tegel_homeiswheremomis.glb`).
- Clicking **Create your own text** switches the viewer to the clean tile (`models/tegel_clean.glb`) and reveals a text input and font selector.
- The code locates a scene node named `TEXT_MAIN` inside the loaded GLB. It uses a 2D canvas to render the typed text and assigns a `THREE.CanvasTexture` to the `TEXT_MAIN` mesh material so the glyphs update live.

Notes for developers
- The customization script is implemented in vanilla JavaScript directly in `index.html` and performs defensive checks when accessing the model scene graph.
- For the live texture approach to work, GLB models must include a mesh named `TEXT_MAIN` whose material accepts a texture map.

How to add new GLB models
1. Place the `.glb` file in the `/models` directory.
2. If the model should support dynamic text, ensure it contains a mesh named `TEXT_MAIN` (case-sensitive).
3. Update `index.html` or the UI logic to reference the new model path where appropriate.

Monthly product rotation workflow
1. Prepare a new GLB for the month and add it to `/models` (include both a clean base and a prefilled text variant if desired).
2. Update marketing text in `plan.txt` and any teasers in `images/`.
3. Replace the `src` used as default in `index.html` when you want a particular design to be featured by default.
4. Optionally, schedule an Etsy listing push and social posts linking to the landing page.

Contact
For technical questions, edit `index.html` where the customization script is located.
