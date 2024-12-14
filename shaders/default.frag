#version 410 core

layout (location = 0) in vec4 fragColor;

in vec2 uv_0;

uniform sampler2D u_texture_0;

void main() {
    vec3 color = texture(u_texture_0, uv_0).rgb;
    gl_FragColor = vec4(color, 1.0);
} 