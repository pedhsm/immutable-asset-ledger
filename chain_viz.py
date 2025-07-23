import numpy as np
import plotly.graph_objects as go
from blockchain import Chain

class ChainVisualizer():

    def __init__(self, data_store):
        """
        Initialize with either a Chain instance or raw list
        :param data_store: Chain object or list of blocks
        """
        # Check if we received a Chain instance
        if isinstance(data_store, Chain):
            self.chain = data_store.chain  # Access the actual list through .chain
        elif isinstance(data_store, list):
            self.chain = data_store
        else:
            raise TypeError("Input must be a Chain instance or list of blocks")
            
        self._hash_index = self._build_hash_index()
        self._prev_hash_index = self._build_prev_hash_index()

    def __build_hash_index(self):
        """Create O(1) lookup index for hashes"""
        return {block['hash'].strip().lower(): block for block in self.chain}

    def _build_prev_hash_index(self):
        """Create reverse index for previous hashes"""
        index = {}
        for block in self.chain:
            prev_hash = block['previous_hash'].strip().lower()
            index.setdefault(prev_hash, []).append(block)
        return index

    def find_by_hash(self, target_hash):
        """ Hash lookup"""
        normalized_hash = target_hash.strip().lower()
        return self._hash_index.get(normalized_hash)

    def get_chain_segment(self, target_hash):
        """
        Pega a cadeia inteira do segmento do hash desejado
        Returns: (previous_blocks, target_block, next_blocks)
        """
        current = self.find_by_hash(target_hash)
        if not current:
            return None, None, None

        # Trace backwards
        previous_blocks = []
        working_block = current
        while working_block['previous_hash'] in self._hash_index:
            prev_block = self._hash_index[working_block['previous_hash'].lower()]
            previous_blocks.insert(0, prev_block)  # Maintain order
            working_block = prev_block

        # Trace forwards
        next_blocks = self._prev_hash_index.get(current['hash'].lower(), [])

        return previous_blocks, current, next_blocks

    def visualize_from_hash(self, target_hash):
        """Visualizacao completa a partir do hash"""
        previous, current, next_blocks = self.get_chain_segment(target_hash)
        
        if not current:
            sample_hashes = [block['hash'][:8] + '...' for block in self.data_store[:3]]
            raise ValueError(f"Hash not found. Sample hashes: {', '.join(sample_hashes)}")

        fig = go.Figure()
        
        fig.add_trace(self._create_node(
            x=0, y=0,
            text=f"🎯 {current['name']}<br>Hash: {current['hash'][:8]}...",
            color='#FF6B6B',
            size=25
        ))

        prev_positions = self._calculate_positions(len(previous), sector=(-np.pi/2, np.pi/2))
        for idx, block in enumerate(previous):
            x, y = prev_positions[idx]
            fig.add_trace(self._create_node(
                x, y,
                f"🡐 {block['name']}<br>Hash: {block['hash'][:8]}...",
                '#4ECDC4'
            ))
            fig.add_trace(self._create_connection(0, 0, x, y))

        next_positions = self._calculate_positions(len(next_blocks), sector=(np.pi/2, 3*np.pi/2))
        for idx, block in enumerate(next_blocks):
            x, y = next_positions[idx]
            fig.add_trace(self._create_node(
                x, y,
                f"🡒 {block['name']}<br>Hash: {block['hash'][:8]}...",
                '#20B2AA'
            ))
            fig.add_trace(self._create_connection(0, 0, x, y))

        fig.update_layout(self._base_layout(title=f"Chain Context: {current['name']}"))
        return fig

    def _create_node(self, x, y, text, color, size=20):
        return go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(size=size, color=color, line=dict(width=2, color='black')),
            text=text,
            textposition='top center',
            hoverinfo='text'
        )

    def _create_connection(self, x0, y0, x1, y1):
        return go.Scatter(
            x=[x0, x1], y=[y0, y1],
            mode='lines',
            line=dict(color='grey', width=1),
            hoverinfo='none'
        )

    def _calculate_positions(self, num_nodes, sector=(0, 2*np.pi), radius=3):
        angles = np.linspace(sector[0], sector[1], num_nodes, endpoint=False)
        return [(radius * np.cos(a), radius * np.sin(a)) for a in angles]

    def _base_layout(self, title):
        return {
            'title': title,
            'showlegend': False,
            'xaxis': {'visible': False},
            'yaxis': {'visible': False},
            'margin': dict(l=20, r=20, t=40, b=20),
            'height': 600,
            'plot_bgcolor': 'rgba(0,0,0,0)'
        }