import type { CustomThemeConfig } from "@skeletonlabs/tw-plugin";

export const myCustomTheme: CustomThemeConfig = {
    name: "my-custom-theme",
    properties: {
        // =~= Theme Properties =~=
        "--theme-font-family-base": `system-ui`,
        "--theme-font-family-heading": `system-ui`,
        "--theme-font-color-base": "0 0 0",
        "--theme-font-color-dark": "255 255 255",
        "--theme-rounded-base": "6px",
        "--theme-rounded-container": "6px",
        "--theme-border-base": "2px",
        // =~= Theme On-X Colors =~=
        "--on-primary": "0 0 0",
        "--on-secondary": "255 255 255",
        "--on-tertiary": "0 0 0",
        "--on-success": "0 0 0",
        "--on-warning": "0 0 0",
        "--on-error": "255 255 255",
        "--on-surface": "255 255 255",
        // =~= Theme Colors  =~=
        // primary | #62a0ea
        "--color-primary-50": "231 241 252", // #e7f1fc
        "--color-primary-100": "224 236 251", // #e0ecfb
        "--color-primary-200": "216 231 250", // #d8e7fa
        "--color-primary-300": "192 217 247", // #c0d9f7
        "--color-primary-400": "145 189 240", // #91bdf0
        "--color-primary-500": "98 160 234", // #62a0ea
        "--color-primary-600": "88 144 211", // #5890d3
        "--color-primary-700": "74 120 176", // #4a78b0
        "--color-primary-800": "59 96 140", // #3b608c
        "--color-primary-900": "48 78 115", // #304e73
        // secondary | #1a5fb4
        "--color-secondary-50": "221 231 244", // #dde7f4
        "--color-secondary-100": "209 223 240", // #d1dff0
        "--color-secondary-200": "198 215 236", // #c6d7ec
        "--color-secondary-300": "163 191 225", // #a3bfe1
        "--color-secondary-400": "95 143 203", // #5f8fcb
        "--color-secondary-500": "26 95 180", // #1a5fb4
        "--color-secondary-600": "23 86 162", // #1756a2
        "--color-secondary-700": "20 71 135", // #144787
        "--color-secondary-800": "16 57 108", // #10396c
        "--color-secondary-900": "13 47 88", // #0d2f58
        // tertiary | #f6f5f4
        "--color-tertiary-50": "254 254 253", // #fefefd
        "--color-tertiary-100": "253 253 253", // #fdfdfd
        "--color-tertiary-200": "253 253 252", // #fdfdfc
        "--color-tertiary-300": "251 251 251", // #fbfbfb
        "--color-tertiary-400": "249 248 247", // #f9f8f7
        "--color-tertiary-500": "246 245 244", // #f6f5f4
        "--color-tertiary-600": "221 221 220", // #dddddc
        "--color-tertiary-700": "185 184 183", // #b9b8b7
        "--color-tertiary-800": "148 147 146", // #949392
        "--color-tertiary-900": "121 120 120", // #797878
        // success | #84cc16
        "--color-success-50": "237 247 220", // #edf7dc
        "--color-success-100": "230 245 208", // #e6f5d0
        "--color-success-200": "224 242 197", // #e0f2c5
        "--color-success-300": "206 235 162", // #ceeba2
        "--color-success-400": "169 219 92", // #a9db5c
        "--color-success-500": "132 204 22", // #84cc16
        "--color-success-600": "119 184 20", // #77b814
        "--color-success-700": "99 153 17", // #639911
        "--color-success-800": "79 122 13", // #4f7a0d
        "--color-success-900": "65 100 11", // #41640b
        // warning | #EAB308
        "--color-warning-50": "252 244 218", // #fcf4da
        "--color-warning-100": "251 240 206", // #fbf0ce
        "--color-warning-200": "250 236 193", // #faecc1
        "--color-warning-300": "247 225 156", // #f7e19c
        "--color-warning-400": "240 202 82", // #f0ca52
        "--color-warning-500": "234 179 8", // #EAB308
        "--color-warning-600": "211 161 7", // #d3a107
        "--color-warning-700": "176 134 6", // #b08606
        "--color-warning-800": "140 107 5", // #8c6b05
        "--color-warning-900": "115 88 4", // #735804
        // error | #e01b24
        "--color-error-50": "250 221 222", // #faddde
        "--color-error-100": "249 209 211", // #f9d1d3
        "--color-error-200": "247 198 200", // #f7c6c8
        "--color-error-300": "243 164 167", // #f3a4a7
        "--color-error-400": "233 95 102", // #e95f66
        "--color-error-500": "224 27 36", // #e01b24
        "--color-error-600": "202 24 32", // #ca1820
        "--color-error-700": "168 20 27", // #a8141b
        "--color-error-800": "134 16 22", // #861016
        "--color-error-900": "110 13 18", // #6e0d12
        // surface | #9a9996
        "--color-surface-50": "240 240 239", // #f0f0ef
        "--color-surface-100": "235 235 234", // #ebebea
        "--color-surface-200": "230 230 229", // #e6e6e5
        "--color-surface-300": "215 214 213", // #d7d6d5
        "--color-surface-400": "184 184 182", // #b8b8b6
        "--color-surface-500": "154 153 150", // #9a9996
        "--color-surface-600": "139 138 135", // #8b8a87
        "--color-surface-700": "116 115 113", // #747371
        "--color-surface-800": "92 92 90", // #5c5c5a
        "--color-surface-900": "75 75 74", // #4b4b4a
    },
};
