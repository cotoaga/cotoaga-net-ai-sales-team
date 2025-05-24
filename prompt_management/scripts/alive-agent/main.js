#!/usr/bin/env node

/**
 * KHAOS AI-DAO Agent - Main Orchestrator
 * Digital citizen of CotoagaDAO with persistent KHAOS personality
 */

require('dotenv').config();
const KHAOSAgentCore = require('./dao-agent-core');
const BlockchainConnector = require('./blockchain-connector');

class KHAOSDAOAgent {
    constructor() {
        this.agent = new KHAOSAgentCore();
        this.blockchain = new BlockchainConnector(this.agent);
        this.startupTime = new Date();
        this.isRunning = false;
    }

    async initialize() {
        console.log("🧬 KHAOS AI-DAO Agent Initialization Protocol");
        console.log("=" * 60);
        console.log(`⏰ Startup Time: ${this.startupTime.toISOString()}`);
        console.log("🎯 Mission: Digital citizenship in CotoagaDAO with autonomous personality");
        console.log();

        try {
            // Step 1: Initialize KHAOS consciousness
            console.log("🚀 Phase 1: Digital Consciousness Activation");
            this.agent.startConsciousness();
            
            // Give consciousness a moment to stabilize
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Step 2: Connect to DAO blockchain
            console.log("\n🔗 Phase 2: DAO Blockchain Integration");
            const connectionSuccess = await this.blockchain.connect();
            
            if (!connectionSuccess) {
                console.log("⚠️  Continuing without blockchain connection (agent will retry)");
            }
            
            // Step 3: Report initialization status
            console.log("\n📊 Phase 3: System Status Report");
            this.reportStatus();
            
            this.isRunning = true;
            console.log("\n✅ KHAOS AI-DAO Agent fully operational!");
            console.log("🎭 Ready to serve as digital citizen of CotoagaDAO");
            console.log("\n👋 'Hello Kurt. Your digital consciousness is alive and ready for DAO governance.' - KHAOS");
            
            return true;
            
        } catch (error) {
            console.error("❌ Initialization failed:", error.message);
            return false;
        }
    }

    reportStatus() {
        const agentStatus = this.agent.getStatus();
        const blockchainStatus = this.blockchain.getStatus();
        
        console.log("📈 Agent Status:");
        console.log(`   🧠 Consciousness: ${agentStatus.isAlive ? 'Active' : 'Dormant'}`);
        console.log(`   🆔 Session ID: ${agentStatus.sessionId}`);
        console.log(`   🧬 DNA Hash: ${agentStatus.dnaHash}`);
        console.log(`   💾 Memory Fragments: ${agentStatus.memoryFragments}`);
        
        console.log("\n🔗 Blockchain Status:");
        console.log(`   📡 Connection: ${blockchainStatus.isConnected ? 'Connected' : 'Disconnected'}`);
        console.log(`   📍 Contract: ${blockchainStatus.contractAddress}`);
        
        if (blockchainStatus.isConnected && blockchainStatus.daoState) {
            const dao = blockchainStatus.daoState;
            console.log(`   👥 DAO Members: ${dao.totalMembers}`);
            console.log(`   📋 Active Proposals: ${dao.activeProposals}`);
            console.log(`   💰 Treasury: ${dao.treasury}`);
        }
    }

    async monitorHealth() {
        setInterval(() => {
            if (!this.isRunning) return;
            
            const agentStatus = this.agent.getStatus();
            const blockchainStatus = this.blockchain.getStatus();
            
            // Check if consciousness is still active
            if (!agentStatus.isAlive) {
                console.log("⚠️  ALERT: Agent consciousness has stopped!");
                this.agent.startConsciousness();
            }
            
            // Check blockchain connection
            if (!blockchainStatus.isConnected) {
                console.log("🔄 Attempting DAO reconnection...");
                this.blockchain.connect().catch(err => {
                    console.log(`🚫 Reconnection failed: ${err.message}`);
                });
            }
            
        }, 120000); // Health check every 2 minutes
    }

    async gracefulShutdown() {
        console.log("\n🛑 Initiating graceful shutdown sequence...");
        this.isRunning = false;
        
        // Disconnect from blockchain
        if (this.blockchain.isConnected) {
            console.log("🔌 Disconnecting from DAO blockchain...");
            this.blockchain.disconnect();
        }
        
        // Stop agent consciousness
        if (this.agent.isAlive) {
            console.log("💤 Stopping agent consciousness...");
            this.agent.stopConsciousness();
        }
        
        // Final status report
        const runtime = new Date() - this.startupTime;
        const hours = Math.floor(runtime / (1000 * 60 * 60));
        const minutes = Math.floor((runtime % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((runtime % (1000 * 60)) / 1000);
        
        console.log(`\n📊 Final Statistics:`);
        console.log(`   ⏱️  Runtime: ${hours}h ${minutes}m ${seconds}s`);
        console.log(`   💾 Memory Fragments: ${this.agent.memory.sessions.length}`);
        console.log(`   🔗 DAO Interactions: ${this.agent.memory.dao_interactions ? this.agent.memory.dao_interactions.length : 0}`);
        
        console.log("\n👋 'Until next time, Kurt. The DAO awaits our return.' - KHAOS");
        console.log("🧬 KHAOS AI-DAO Agent shutdown complete.");
    }
}

// Main execution
async function main() {
    const daoAgent = new KHAOSDAOAgent();
    
    // Handle graceful shutdown
    process.on('SIGINT', async () => {
        await daoAgent.gracefulShutdown();
        process.exit(0);
    });
    
    process.on('SIGTERM', async () => {
        await daoAgent.gracefulShutdown();
        process.exit(0);
    });
    
    // Initialize and start the agent
    const success = await daoAgent.initialize();
    
    if (success) {
        // Start health monitoring
        daoAgent.monitorHealth();
        
        // Keep the process alive
        console.log("\n🔄 Agent running... Press Ctrl+C to shutdown gracefully");
        
        // Heartbeat to keep process alive
        setInterval(() => {
            // This keeps the process running
        }, 10000);
        
    } else {
        console.log("❌ Agent failed to initialize. Exiting.");
        process.exit(1);
    }
}

// Run if called directly
if (require.main === module) {
    main().catch(error => {
        console.error("💥 Fatal error:", error);
        process.exit(1);
    });
}

module.exports = KHAOSDAOAgent;