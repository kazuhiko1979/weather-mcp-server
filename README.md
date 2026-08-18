# Weather MCP Server

National Weather Service (NWS) のアクティブな気象警報を取得する MCP サーバーです。

## セットアップ

\`\`\`bash
uv sync
\`\`\`

## 起動

stdio トランスポートで起動します。

\`\`\`bash
uv run weather.py
\`\`\`

このプロセスは MCP クライアントからの JSON-RPC メッセージを待機します。
通常の文字列を標準入力へ直接入力するのではなく、Codex などの MCP クライアントから接続してください。

## 提供ツール

### \`get_weather\`

米国の州コード（例: \`CA\`、\`GA\`）を指定すると、その州のアクティブな気象警報を返します。

## Codex への登録

\`\`\`bash
codex mcp add weather -- \
  uv --directory /home/kazuh/project/workspaces/weather run weather.py
\`\`\`
