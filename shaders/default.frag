#version 410 core

layout (location = 0) in vec4 fragColor;

void main() {
    vec3 color = vec3(1,0,0);
    gl_FragColor = vec4(color, 1.0);
} 